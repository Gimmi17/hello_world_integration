"""Sensor platform for Hello World integration."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.info("Setting up Hello World sensor")
    
    name = config_entry.data.get("name", "Hello World")
    async_add_entities([HelloWorldSensor(name)], True)


class HelloWorldSensor(SensorEntity):
    """Hello World sensor."""

    def __init__(self, name: str) -> None:
        """Initialize the sensor."""
        self._name = name
        self._state = "Hello, World! 👋"
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional state attributes."""
        return {
            "message": "Hello from your custom Home Assistant integration!",
            "last_updated": datetime.now().isoformat(),
            "integration_domain": DOMAIN,
        }

    @property
    def icon(self) -> str:
        """Return the icon to use for the sensor."""
        return "mdi:hand-wave" 