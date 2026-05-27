from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Callable

from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICE_NAME, CONF_TOPIC_PREFIX, DOMAIN


@dataclass(frozen=True)
class SensorDef:
  key: str
  name: str
  icon: str
  unit: str | None = None


SENSORS: tuple[SensorDef, ...] = (
  SensorDef("proximoHora", "Proxima toma hora", "mdi:clock-outline"),
  SensorDef("proximoMedicamentos", "Proxima toma medicamentos", "mdi:pill"),
  SensorDef("horarios", "Cantidad horarios", "mdi:calendar-multiple", "horarios"),
  SensorDef("diasRestantes", "Dias restantes", "mdi:calendar-clock", "dias"),
  SensorDef("compartimentosRestantes", "Compartimentos restantes", "mdi:tray-full"),
  SensorDef("compartimentosMaximos", "Compartimentos maximos", "mdi:counter"),
  SensorDef("compartimentoActual", "Compartimento actual", "mdi:rotate-3d-variant"),
  SensorDef("horariosDetalleTexto", "Horarios y medicamentos", "mdi:format-list-bulleted"),
)


class MediControlHub:
  def __init__(self, hass: HomeAssistant, topic_prefix: str) -> None:
    self.hass = hass
    self.topic_prefix = topic_prefix
    self.state: dict[str, Any] = {}
    self._listeners: list[Callable[[], None]] = []
    self._unsub: Callable[[], None] | None = None

  async def async_start(self) -> None:
    topic = f"{self.topic_prefix}/medicamentos"

    @callback
    def _message_received(msg: mqtt.ReceiveMessage) -> None:
      parsed: dict[str, Any] | None = None
      if isinstance(msg.payload, str):
        try:
          candidate = json.loads(msg.payload)
          if isinstance(candidate, dict):
            parsed = candidate
        except json.JSONDecodeError:
          parsed = None
      if parsed is None:
        return
      self.state = parsed
      for listener in self._listeners:
        listener()

    self._unsub = await mqtt.async_subscribe(self.hass, topic, _message_received, qos=0)

  async def async_stop(self) -> None:
    if self._unsub is not None:
      self._unsub()
      self._unsub = None

  def add_listener(self, listener: Callable[[], None]) -> Callable[[], None]:
    self._listeners.append(listener)

    def _remove() -> None:
      if listener in self._listeners:
        self._listeners.remove(listener)

    return _remove


async def async_setup_entry(
  hass: HomeAssistant,
  entry: ConfigEntry,
  async_add_entities: AddEntitiesCallback,
) -> None:
  topic_prefix = entry.data[CONF_TOPIC_PREFIX].strip().strip("/")
  device_name = entry.data[CONF_DEVICE_NAME]

  hub = MediControlHub(hass, topic_prefix)
  await hub.async_start()
  hass.data[DOMAIN][entry.entry_id]["hub"] = hub

  entities = [MediControlSensor(hub, entry, device_name, topic_prefix, sd) for sd in SENSORS]
  async_add_entities(entities)


class MediControlSensor(SensorEntity):
  _attr_has_entity_name = True

  def __init__(
    self,
    hub: MediControlHub,
    entry: ConfigEntry,
    device_name: str,
    topic_prefix: str,
    sensor_def: SensorDef,
  ) -> None:
    self._hub = hub
    self._entry = entry
    self._def = sensor_def
    self._attr_name = sensor_def.name
    self._attr_unique_id = f"{entry.entry_id}_{sensor_def.key}"
    self._attr_icon = sensor_def.icon
    self._attr_native_unit_of_measurement = sensor_def.unit
    self._attr_device_info = {
      "identifiers": {(DOMAIN, topic_prefix)},
      "name": device_name,
      "manufacturer": "NeoDesarrollos.com",
      "model": "MediControl",
    }
    self._remove_listener: Callable[[], None] | None = None

  @property
  def native_value(self) -> Any:
    if self._def.key == "horariosDetalleTexto":
      detalle = self._hub.state.get("horariosDetalle")
      if not isinstance(detalle, list) or len(detalle) == 0:
        return "Sin horarios"
      lineas: list[str] = []
      for item in detalle:
        if not isinstance(item, dict):
          continue
        hora = str(item.get("hora", "--:--"))
        meds = item.get("medicamentos", [])
        if isinstance(meds, list) and len(meds) > 0:
          meds_txt = ", ".join(str(m) for m in meds)
        else:
          meds_txt = "Sin medicamentos"
        lineas.append(f"{hora}: {meds_txt}")
      return " | ".join(lineas) if len(lineas) > 0 else "Sin horarios"
    if self._def.key == "proximoHora":
      return self._hub.state.get("proximoHora") or self._hub.state.get("proximo")
    if self._def.key == "proximoMedicamentos":
      return self._hub.state.get("proximoMedicamentos") or self._hub.state.get("lista")
    return self._hub.state.get(self._def.key)

  @property
  def available(self) -> bool:
    return bool(self._hub.state)

  async def async_added_to_hass(self) -> None:
    self._remove_listener = self._hub.add_listener(self.async_write_ha_state)

  async def async_will_remove_from_hass(self) -> None:
    if self._remove_listener is not None:
      self._remove_listener()
      self._remove_listener = None
