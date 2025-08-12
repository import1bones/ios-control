"""
iOS Device Control Module

Provides the main IOSDevice class for controlling iOS devices.
"""

import subprocess
import json
import time
from typing import Optional, List, Dict, Any, Tuple
from .exceptions import (
    DeviceNotFoundError,
    IOSConnectionError,
    UnsupportedOperationError,
)


class IOSDevice:
    """
    Main class for controlling iOS devices.

    This class provides methods to connect to and control iOS devices
    using various iOS communication protocols and tools.
    """

    def __init__(self, udid: Optional[str] = None):
        """
        Initialize iOS device controller.

        Args:
            udid: Specific device UDID to connect to. If None, will use first available device.
        """
        self.udid = udid
        self._device_info: Optional[Dict[str, Any]] = None
        self._connected = False

    def connect(self) -> bool:
        """
        Connect to the iOS device.

        Returns:
            True if connection successful, False otherwise.

        Raises:
            DeviceNotFoundError: If no device found.
            IOSConnectionError: If connection fails.
        """
        try:
            devices = self.list_devices()
            if not devices:
                raise DeviceNotFoundError("No iOS devices found")

            if self.udid:
                device = next((d for d in devices if d.get("udid") == self.udid), None)
                if not device:
                    raise DeviceNotFoundError(f"Device with UDID {self.udid} not found")
            else:
                device = devices[0]
                self.udid = device.get("udid")

            self._device_info = device
            self._connected = True
            return True

        except Exception as e:
            raise IOSConnectionError(f"Failed to connect to device: {str(e)}")

    def disconnect(self) -> None:
        """Disconnect from the iOS device."""
        self._connected = False
        self._device_info = None

    @property
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self._connected

    @property
    def device_info(self) -> Optional[Dict[str, Any]]:
        """Get device information."""
        return self._device_info

    @staticmethod
    def list_devices() -> List[Dict[str, Any]]:
        """
        List all available iOS devices.

        Returns:
            List of device information dictionaries.
        """
        try:
            # Try using idevice_id from libimobiledevice
            result = subprocess.run(
                ["idevice_id", "-l"], capture_output=True, text=True, check=True
            )
            device_ids = result.stdout.strip().split("\n")
            device_ids = [uid for uid in device_ids if uid]

            devices = []
            for udid in device_ids:
                try:
                    # Get device name
                    name_result = subprocess.run(
                        ["ideviceinfo", "-u", udid, "-k", "DeviceName"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    device_name = name_result.stdout.strip()

                    # Get device version
                    version_result = subprocess.run(
                        ["ideviceinfo", "-u", udid, "-k", "ProductVersion"],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    ios_version = version_result.stdout.strip()

                    devices.append(
                        {"udid": udid, "name": device_name, "ios_version": ios_version}
                    )
                except subprocess.CalledProcessError:
                    # If we can't get device info, add basic info
                    devices.append(
                        {
                            "udid": udid,
                            "name": "Unknown Device",
                            "ios_version": "Unknown",
                        }
                    )

            return devices

        except subprocess.CalledProcessError:
            # Fall back to checking if any devices via other methods
            return []
        except FileNotFoundError:
            # libimobiledevice tools not installed
            return []

    def get_device_info(self) -> Dict[str, Any]:
        """
        Get detailed device information.

        Returns:
            Dictionary containing device information.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            result = subprocess.run(
                ["ideviceinfo", "-u", self.udid],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the output into a dictionary
            info = {}
            for line in result.stdout.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    info[key.strip()] = value.strip()

            return info

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to get device info: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("libimobiledevice tools not installed")

    def install_app(self, ipa_path: str) -> bool:
        """
        Install an app on the device.

        Args:
            ipa_path: Path to the IPA file to install.

        Returns:
            True if installation successful.

        Raises:
            IOSConnectionError: If device not connected.
            UnsupportedOperationError: If operation not supported.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            subprocess.run(
                ["ideviceinstaller", "-u", self.udid, "-i", ipa_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to install app: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("ideviceinstaller not installed")

    def uninstall_app(self, bundle_id: str) -> bool:
        """
        Uninstall an app from the device.

        Args:
            bundle_id: Bundle identifier of the app to uninstall.

        Returns:
            True if uninstallation successful.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            subprocess.run(
                ["ideviceinstaller", "-u", self.udid, "-U", bundle_id],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to uninstall app: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("ideviceinstaller not installed")

    def list_apps(self) -> List[Dict[str, str]]:
        """
        List installed apps on the device.

        Returns:
            List of app information dictionaries.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            result = subprocess.run(
                ["ideviceinstaller", "-u", self.udid, "-l"],
                capture_output=True,
                text=True,
                check=True,
            )

            apps = []
            for line in result.stdout.split("\n"):
                if " - " in line:
                    parts = line.split(" - ", 1)
                    if len(parts) == 2:
                        bundle_id = parts[0].strip()
                        app_name = parts[1].strip()
                        apps.append({"bundle_id": bundle_id, "name": app_name})

            return apps

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to list apps: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("ideviceinstaller not installed")

    def reboot(self) -> bool:
        """
        Reboot the iOS device.

        Returns:
            True if reboot command sent successfully.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            subprocess.run(
                ["idevicediagnostics", "-u", self.udid, "restart"],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to reboot device: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("idevicediagnostics not installed")

    def screenshot(self, output_path: str = "screenshot.png") -> str:
        """
        Take a screenshot of the device.

        Args:
            output_path: Path where to save the screenshot.

        Returns:
            Path to the saved screenshot.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            subprocess.run(
                ["idevicescreenshot", "-u", self.udid, output_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return output_path

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to take screenshot: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("idevicescreenshot not installed")

    def tap(self, x: int, y: int) -> bool:
        """
        Tap at specific coordinates on the device screen.

        Args:
            x: X coordinate to tap
            y: Y coordinate to tap

        Returns:
            True if tap successful.

        Raises:
            IOSConnectionError: If device not connected.
            UnsupportedOperationError: If required tools not available.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Using pymobiledevice3 for UI automation
            subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "tap",
                    "--udid",
                    self.udid,
                    str(x),
                    str(y),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            # Try alternative method with idevice tools if available
            try:
                # Alternative: use tidevice if available
                subprocess.run(
                    ["tidevice", "--udid", self.udid, "tap", str(x), str(y)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise IOSConnectionError(f"Failed to tap at ({x}, {y}): {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError(
                "Neither pymobiledevice3 nor tidevice is available for UI automation"
            )

    def swipe(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5
    ) -> bool:
        """
        Swipe from one point to another on the device screen.

        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Duration of swipe in seconds (default: 0.5)

        Returns:
            True if swipe successful.

        Raises:
            IOSConnectionError: If device not connected.
            UnsupportedOperationError: If required tools not available.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Using pymobiledevice3 for UI automation
            subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "swipe",
                    "--udid",
                    self.udid,
                    str(start_x),
                    str(start_y),
                    str(end_x),
                    str(end_y),
                    "--duration",
                    str(duration),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            # Try alternative method
            try:
                subprocess.run(
                    [
                        "tidevice",
                        "--udid",
                        self.udid,
                        "swipe",
                        str(start_x),
                        str(start_y),
                        str(end_x),
                        str(end_y),
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise IOSConnectionError(f"Failed to swipe: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError(
                "Neither pymobiledevice3 nor tidevice is available for UI automation"
            )

    def input_text(self, text: str) -> bool:
        """
        Input text on the device (types into currently focused text field).

        Args:
            text: Text to input

        Returns:
            True if text input successful.

        Raises:
            IOSConnectionError: If device not connected.
            UnsupportedOperationError: If required tools not available.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Using pymobiledevice3 for text input
            subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "input",
                    "--udid",
                    self.udid,
                    text,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            # Try alternative method
            try:
                subprocess.run(
                    ["tidevice", "--udid", self.udid, "input", text],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise IOSConnectionError(f"Failed to input text: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError(
                "Neither pymobiledevice3 nor tidevice is available for UI automation"
            )

    def tap_by_text(self, text: str, exact_match: bool = False) -> bool:
        """
        Tap on an element containing specific text.

        Args:
            text: Text to search for and tap
            exact_match: If True, requires exact text match. If False, partial match.

        Returns:
            True if element found and tapped.

        Raises:
            IOSConnectionError: If device not connected.
            UnsupportedOperationError: If required tools not available.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # First, get the UI hierarchy to find elements with the text
            ui_info = self._get_ui_hierarchy()

            # Find element coordinates by text
            coordinates = self._find_element_by_text(ui_info, text, exact_match)

            if coordinates:
                x, y = coordinates
                return self.tap(x, y)
            else:
                raise IOSConnectionError(f"Element with text '{text}' not found")

        except Exception as e:
            raise IOSConnectionError(f"Failed to tap by text '{text}': {str(e)}")

    def _get_ui_hierarchy(self) -> Dict:
        """
        Get the UI hierarchy of the current screen.

        Returns:
            Dictionary containing UI hierarchy information.
        """
        try:
            # Try using pymobiledevice3 to get UI hierarchy
            result = subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "ui",
                    "--udid",
                    self.udid,
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            return json.loads(result.stdout)

        except subprocess.CalledProcessError:
            # Try alternative methods
            try:
                # Alternative: use tidevice dump
                result = subprocess.run(
                    ["tidevice", "--udid", self.udid, "dump-hierarchy"],
                    capture_output=True,
                    text=True,
                    check=True,
                )

                # Parse the output (format may vary)
                return {"hierarchy": result.stdout}

            except (subprocess.CalledProcessError, FileNotFoundError):
                raise UnsupportedOperationError("Cannot get UI hierarchy")
        except FileNotFoundError:
            raise UnsupportedOperationError("UI automation tools not available")

    def _find_element_by_text(
        self, ui_info: Dict, text: str, exact_match: bool = False
    ) -> Optional[Tuple[int, int]]:
        """
        Find element coordinates by text in UI hierarchy.

        Args:
            ui_info: UI hierarchy information
            text: Text to search for
            exact_match: Whether to use exact text matching

        Returns:
            Tuple of (x, y) coordinates if found, None otherwise.
        """

        def search_recursive(element):
            if isinstance(element, dict):
                # Check if this element has text
                element_text = (
                    element.get("text", "")
                    or element.get("label", "")
                    or element.get("name", "")
                )

                if element_text:
                    if exact_match:
                        if element_text == text:
                            # Get element bounds/coordinates
                            bounds = element.get("bounds") or element.get("frame")
                            if bounds:
                                return self._get_center_coordinates(bounds)
                    else:
                        if text.lower() in element_text.lower():
                            bounds = element.get("bounds") or element.get("frame")
                            if bounds:
                                return self._get_center_coordinates(bounds)

                # Search in children
                children = element.get("children", []) or element.get("elements", [])
                for child in children:
                    result = search_recursive(child)
                    if result:
                        return result

            elif isinstance(element, list):
                for item in element:
                    result = search_recursive(item)
                    if result:
                        return result

            return None

        return search_recursive(ui_info)

    def _get_center_coordinates(self, bounds) -> Tuple[int, int]:
        """
        Get center coordinates from element bounds.

        Args:
            bounds: Bounds information (can be various formats)

        Returns:
            Tuple of center (x, y) coordinates.
        """
        if isinstance(bounds, dict):
            # Handle different bound formats
            if (
                "x" in bounds
                and "y" in bounds
                and "width" in bounds
                and "height" in bounds
            ):
                # Format: {x: int, y: int, width: int, height: int}
                x = bounds["x"] + bounds["width"] // 2
                y = bounds["y"] + bounds["height"] // 2
                return (x, y)
            elif (
                "left" in bounds
                and "top" in bounds
                and "right" in bounds
                and "bottom" in bounds
            ):
                # Format: {left: int, top: int, right: int, bottom: int}
                x = (bounds["left"] + bounds["right"]) // 2
                y = (bounds["top"] + bounds["bottom"]) // 2
                return (x, y)
        elif isinstance(bounds, (list, tuple)) and len(bounds) >= 4:
            # Format: [x, y, width, height] or [left, top, right, bottom]
            x = (bounds[0] + bounds[2]) // 2
            y = (bounds[1] + bounds[3]) // 2
            return (x, y)

        # Default fallback
        return (100, 100)

    def long_press(self, x: int, y: int, duration: float = 1.0) -> bool:
        """
        Long press at specific coordinates.

        Args:
            x: X coordinate to long press
            y: Y coordinate to long press
            duration: Duration of press in seconds (default: 1.0)

        Returns:
            True if long press successful.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Using pymobiledevice3 for long press
            subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "longpress",
                    "--udid",
                    self.udid,
                    str(x),
                    str(y),
                    "--duration",
                    str(duration),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            raise IOSConnectionError(f"Failed to long press at ({x}, {y}): {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError(
                "pymobiledevice3 not available for UI automation"
            )

    def home_button(self) -> bool:
        """
        Press the home button.

        Returns:
            True if home button press successful.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Using pymobiledevice3 for home button
            subprocess.run(
                [
                    "python3",
                    "-m",
                    "pymobiledevice3",
                    "developer",
                    "dvt",
                    "home",
                    "--udid",
                    self.udid,
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            # Try alternative method
            try:
                subprocess.run(
                    ["tidevice", "--udid", self.udid, "home"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise IOSConnectionError(f"Failed to press home button: {str(e)}")
        except FileNotFoundError:
            raise UnsupportedOperationError("UI automation tools not available")

    def back_button(self) -> bool:
        """
        Press the back button (swipe from left edge).

        Returns:
            True if back gesture successful.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        # Simulate back gesture by swiping from left edge
        # Get screen dimensions first (assume common iPhone dimensions if not available)
        try:
            # Swipe from left edge to center
            return self.swipe(10, 300, 200, 300, 0.3)
        except Exception as e:
            raise IOSConnectionError(f"Failed to perform back gesture: {str(e)}")

    def wait_for_element_by_text(
        self, text: str, timeout: int = 10, exact_match: bool = False
    ) -> bool:
        """
        Wait for an element with specific text to appear.

        Args:
            text: Text to wait for
            timeout: Maximum time to wait in seconds
            exact_match: Whether to use exact text matching

        Returns:
            True if element appears within timeout.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                ui_info = self._get_ui_hierarchy()
                coordinates = self._find_element_by_text(ui_info, text, exact_match)

                if coordinates:
                    return True

                time.sleep(0.5)  # Wait before next check

            except Exception:
                time.sleep(0.5)
                continue

        return False

    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get the screen size of the device.

        Returns:
            Tuple of (width, height) in pixels.

        Raises:
            IOSConnectionError: If device not connected.
        """
        if not self.is_connected:
            raise IOSConnectionError("Device not connected")

        try:
            # Get device info to determine screen size
            info = self.get_device_info()
            product_type = info.get("ProductType", "")

            # Common iPhone/iPad screen sizes (in points, need to multiply by scale factor)
            screen_sizes = {
                "iPhone16,2": (393, 852),  # iPhone 15 Pro
                "iPhone16,1": (393, 852),  # iPhone 15
                "iPhone15,5": (428, 926),  # iPhone 14 Plus
                "iPhone15,4": (390, 844),  # iPhone 14
                "iPhone14,3": (428, 926),  # iPhone 13 Pro Max
                "iPhone14,2": (390, 844),  # iPhone 13 Pro
                "iPhone13,4": (428, 926),  # iPhone 12 Pro Max
                "iPhone13,3": (390, 844),  # iPhone 12 Pro
                "iPad14,6": (1024, 1366),  # iPad Air 5th gen
                "iPad13,11": (1024, 1366),  # iPad Pro 12.9"
            }

            return screen_sizes.get(product_type, (375, 667))  # Default iPhone size

        except Exception:
            # Return default iPhone screen size if detection fails
            return (375, 667)

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

    def __str__(self) -> str:
        """String representation of the device."""
        if self._device_info:
            return f"IOSDevice(udid={self.udid}, name={self._device_info.get('name', 'Unknown')})"
        return f"IOSDevice(udid={self.udid}, connected={self.is_connected})"
