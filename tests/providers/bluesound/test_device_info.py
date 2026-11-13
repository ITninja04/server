"""
Tests for the device identity a BluOS player reports.

mDNS only carries the model code (N132) and the provider used to name the platform (BluOS)
as the manufacturer, so a NODE showed up as "BluOS N132" and could never match a model based
default icon. SyncStatus names the brand and the product, and those must reach DeviceInfo.
"""

from __future__ import annotations

from typing import cast
from unittest.mock import MagicMock

from music_assistant_models.player import DeviceInfo

from music_assistant.providers.bluesound.player import BluesoundPlayer


def _device_info_after_sync(brand: str, model: str, model_name: str) -> DeviceInfo:
    """Apply a SyncStatus identity to a player that was discovered over mDNS."""
    fake = MagicMock()
    fake._attr_device_info = DeviceInfo(model="N132", manufacturer="BluOS")
    fake.sync_status.brand = brand
    fake.sync_status.model = model
    fake.sync_status.model_name = model_name
    BluesoundPlayer._update_device_info(cast("BluesoundPlayer", fake))
    return cast("DeviceInfo", fake._attr_device_info)


def test_sync_status_identity_replaces_mdns_identity() -> None:
    """Values as reported by a NODE on BluOS 4.18.18 (SyncStatus, 2026-11-13)."""
    device_info = _device_info_after_sync("Bluesound", "N132", "NODE")

    assert device_info.manufacturer == "Bluesound"
    assert device_info.model == "NODE"
    assert device_info.model_id == "N132"


def test_speaker_identity_from_a_pulse_flex() -> None:
    """Values as reported by a Pulse Flex on BluOS 4.18.18 (SyncStatus, 2026-11-13)."""
    device_info = _device_info_after_sync("Bluesound", "P130", "PULSE FLEX")

    assert device_info.manufacturer == "Bluesound"
    assert device_info.model == "PULSE FLEX"
    assert device_info.model_id == "P130"


def test_empty_sync_status_fields_keep_the_mdns_values() -> None:
    """A firmware that leaves the fields out must not blank the identity we already have."""
    device_info = _device_info_after_sync("", "", "")

    assert device_info.manufacturer == "BluOS"
    assert device_info.model == "N132"
    assert device_info.model_id is None
