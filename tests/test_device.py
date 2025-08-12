"""
Tests for iOS device functionality.
"""

import pytest
from unittest.mock import MagicMock
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError
from ios_control.exceptions import UnsupportedOperationError


class TestIOSDevice:
    """Test cases for IOSDevice class."""

    def test_init_with_udid(self):
        """Test device initialization with UDID."""
        device = IOSDevice(udid="test-udid")
        assert device.udid == "test-udid"
        assert not device.is_connected

    def test_init_without_udid(self):
        """Test device initialization without UDID."""
        device = IOSDevice()
        assert device.udid is None
        assert not device.is_connected

    def test_list_devices_success(self, mock_subprocess):
        """Test successful device listing."""
        # Mock successful idevice_id call
        mock_subprocess.run.side_effect = [
            MagicMock(stdout="test-udid-123\ntest-udid-456\n", returncode=0),
            MagicMock(stdout="Test iPhone\n", returncode=0),
            MagicMock(stdout="17.0\n", returncode=0),
            MagicMock(stdout="Test iPad\n", returncode=0),
            MagicMock(stdout="16.5\n", returncode=0),
        ]

        devices = IOSDevice.list_devices()

        assert len(devices) == 2
        assert devices[0]["udid"] == "test-udid-123"
        assert devices[0]["name"] == "Test iPhone"
        assert devices[0]["ios_version"] == "17.0"

    def test_list_devices_no_tools(self, mock_subprocess):
        """Test device listing when tools are not installed."""
        mock_subprocess.run.side_effect = FileNotFoundError()

        devices = IOSDevice.list_devices()
        assert devices == []

    def test_connect_success(self, ios_device, mock_subprocess, mock_device_list):
        """Test successful device connection."""
        with pytest.MonkeyPatch().context() as m:
            m.setattr(IOSDevice, "list_devices", lambda: mock_device_list)

            result = ios_device.connect()

            assert result is True
            assert ios_device.is_connected
            assert ios_device.udid == "test-udid-123"

    def test_connect_device_not_found(self, ios_device, mock_subprocess):
        """Test connection when device is not found."""
        with pytest.MonkeyPatch().context() as m:
            m.setattr(IOSDevice, "list_devices", lambda: [])

            with pytest.raises(DeviceNotFoundError):
                ios_device.connect()

    def test_connect_specific_device_not_found(self, mock_subprocess):
        """Test connection when specific device UDID is not found."""
        device = IOSDevice(udid="non-existent-udid")
        mock_devices = [{"udid": "other-udid", "name": "Other Device"}]

        with pytest.MonkeyPatch().context() as m:
            m.setattr(IOSDevice, "list_devices", lambda: mock_devices)

            with pytest.raises(DeviceNotFoundError):
                device.connect()

    def test_disconnect(self, ios_device):
        """Test device disconnection."""
        ios_device._connected = True
        ios_device._device_info = {"test": "data"}

        ios_device.disconnect()

        assert not ios_device.is_connected
        assert ios_device._device_info is None

    def test_get_device_info_success(self, ios_device, mock_subprocess):
        """Test successful device info retrieval."""
        ios_device._connected = True
        mock_subprocess.run.return_value = MagicMock(
            stdout="DeviceName: Test iPhone\nProductVersion: 17.0\n", returncode=0
        )

        info = ios_device.get_device_info()

        assert info["DeviceName"] == "Test iPhone"
        assert info["ProductVersion"] == "17.0"

    def test_get_device_info_not_connected(self, ios_device):
        """Test device info retrieval when not connected."""
        with pytest.raises(IOSConnectionError):
            ios_device.get_device_info()

    def test_install_app_success(self, ios_device, mock_subprocess):
        """Test successful app installation."""
        ios_device._connected = True
        mock_subprocess.run.return_value = MagicMock(returncode=0)

        result = ios_device.install_app("/path/to/app.ipa")

        assert result is True

    def test_install_app_not_connected(self, ios_device):
        """Test app installation when not connected."""
        with pytest.raises(IOSConnectionError):
            ios_device.install_app("/path/to/app.ipa")

    def test_install_app_tools_missing(self, ios_device, mock_subprocess):
        """Test app installation when tools are missing."""
        ios_device._connected = True
        mock_subprocess.run.side_effect = FileNotFoundError()

        with pytest.raises(UnsupportedOperationError):
            ios_device.install_app("/path/to/app.ipa")

    def test_context_manager(self, ios_device, mock_device_list):
        """Test context manager functionality."""
        with pytest.MonkeyPatch().context() as m:
            m.setattr(IOSDevice, "list_devices", lambda: mock_device_list)

            with ios_device as device:
                assert device.is_connected

            assert not device.is_connected

    def test_str_representation(self, ios_device):
        """Test string representation of device."""
        ios_device._device_info = {"name": "Test iPhone"}
        result = str(ios_device)

        assert "Test iPhone" in result
        assert "test-udid-123" in result
