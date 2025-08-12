"""
iOS Control Library

A Python library for controlling iOS devices programmatically.
"""

from .device import IOSDevice
from .exceptions import IOSControlError, DeviceNotFoundError, IOSConnectionError

__version__ = "0.1.0"
__all__ = ["IOSDevice", "IOSControlError", "DeviceNotFoundError", "IOSConnectionError"]
