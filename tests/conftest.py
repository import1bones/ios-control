"""
Test configuration and fixtures for ios-control tests.
"""

import pytest
from unittest.mock import patch
from ios_control import IOSDevice


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for testing without actual device interaction."""
    with patch("ios_control.device.subprocess") as mock:
        yield mock


@pytest.fixture
def mock_device_list():
    """Mock device list response."""
    return [{"udid": "test-udid-123", "name": "Test iPhone", "ios_version": "17.0"}]


@pytest.fixture
def ios_device():
    """Create an IOSDevice instance for testing."""
    return IOSDevice(udid="test-udid-123")
