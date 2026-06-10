from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}
  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
  if ok:
    entry_data = hass.data[DOMAIN].pop(entry.entry_id, None)
    if entry_data and entry_data.get("hub"):
      await entry_data["hub"].async_stop()
  return ok
