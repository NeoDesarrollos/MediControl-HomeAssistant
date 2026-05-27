from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_DEVICE_NAME, CONF_TOPIC_PREFIX, DEFAULT_DEVICE_NAME, DEFAULT_TOPIC_PREFIX, DOMAIN


class MediControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  VERSION = 1

  async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
    errors: dict[str, str] = {}

    if user_input is not None:
      await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_TOPIC_PREFIX]}")
      self._abort_if_unique_id_configured()
      return self.async_create_entry(title=user_input[CONF_DEVICE_NAME], data=user_input)

    schema = vol.Schema(
      {
        vol.Required(CONF_DEVICE_NAME, default=DEFAULT_DEVICE_NAME): str,
        vol.Required(CONF_TOPIC_PREFIX, default=DEFAULT_TOPIC_PREFIX): str,
      }
    )
    return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
