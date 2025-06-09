"""Update platform for Hello World integration."""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

# GitHub repository info - MODIFICA QUESTI VALORI
GITHUB_REPO = "yourusername/hello_world_integration"
UPDATE_INTERVAL = timedelta(hours=1)  # Controlla ogni ora


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the update platform."""
    coordinator = HelloWorldUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([HelloWorldUpdateEntity(coordinator, config_entry)], True)


class HelloWorldUpdateCoordinator(DataUpdateCoordinator):
    """Update coordinator for checking GitHub releases."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Hello World Update",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest release info from GitHub."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "latest_version": data.get("tag_name", "").lstrip("v"),
                            "release_url": data.get("html_url", ""),
                            "release_notes": data.get("body", ""),
                            "published_at": data.get("published_at", ""),
                        }
                    else:
                        _LOGGER.warning(f"GitHub API returned status {response.status}")
                        return {}
        except Exception as err:
            raise UpdateFailed(f"Error fetching release info: {err}")


class HelloWorldUpdateEntity(UpdateEntity):
    """Hello World update entity."""

    def __init__(
        self,
        coordinator: HelloWorldUpdateCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the update entity."""
        self.coordinator = coordinator
        self.config_entry = config_entry
        self._attr_unique_id = f"{DOMAIN}_update"
        self._attr_name = "Update_checker"
        self._attr_supported_features = UpdateEntityFeature.RELEASE_NOTES

    @property
    def installed_version(self) -> str | None:
        """Return the installed version."""
        # Legge versione dal manifest.json
        try:
            import os
            manifest_path = os.path.join(
                os.path.dirname(__file__), "manifest.json"
            )
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
                return manifest.get("version", "unknown")
        except Exception:
            return "unknown"

    @property
    def latest_version(self) -> str | None:
        """Return the latest version."""
        if self.coordinator.data:
            return self.coordinator.data.get("latest_version")
        return None

    @property
    def release_summary(self) -> str | None:
        """Return the release summary."""
        if self.coordinator.data:
            return f"Aggiornamento disponibile su GitHub"
        return None

    @property
    def release_url(self) -> str | None:
        """Return the release URL."""
        if self.coordinator.data:
            return self.coordinator.data.get("release_url")
        return None

    @property
    def title(self) -> str:
        """Return the title."""
        return self._attr_name

    async def async_release_notes(self) -> str | None:
        """Return the release notes."""
        if self.coordinator.data:
            notes = self.coordinator.data.get("release_notes", "")
            if notes:
                return notes
            return "Nessuna nota di rilascio disponibile."
        return None

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Install the update."""
        # Per ora non implementiamo l'installazione automatica
        # L'utente dovrà fare git pull manualmente
        _LOGGER.info("Update install requested - user should run git pull manually")
        
        # Potresti implementare qui l'esecuzione di git pull automatico
        # Ma per sicurezza è meglio che l'utente lo faccia manualmente

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh() 