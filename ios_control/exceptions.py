"""
Custom exceptions for iOS Control Library
"""


class IOSControlError(Exception):
    """Base exception for iOS Control operations"""

    pass


class DeviceNotFoundError(IOSControlError):
    """Raised when no iOS device is found or device becomes unavailable"""

    pass


class IOSConnectionError(IOSControlError):
    """Raised when connection to iOS device fails"""

    pass


class AuthenticationError(IOSControlError):
    """Raised when device authentication fails"""

    pass


class UnsupportedOperationError(IOSControlError):
    """Raised when attempting an unsupported operation on the device"""

    pass
