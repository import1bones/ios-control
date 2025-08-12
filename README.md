# iOS Control

A Python library for controlling iOS devices programmatically. This library provides an easy-to-use interface for connecting to iOS devices and performing various operations like app management, device information retrieval, and basic device control.

## Features

- **Device Discovery**: Automatically find and connect to iOS devices
- **App Management**: Install, uninstall, and list applications
- **Device Information**: Retrieve detailed device information
- **Screenshots**: Capture device screenshots
- **Device Control**: Reboot devices and more
- **UI Automation**: Tap, swipe, input text, and interact with UI elements
- **Text-based Interaction**: Find and tap elements by their text content
- **Gesture Support**: Tap, long press, swipe, and navigation gestures

## Installation

### Prerequisites

This library requires `libimobiledevice` tools to be installed on your system:

**macOS:**
```bash
brew install libimobiledevice
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libimobiledevice6 libimobiledevice-utils
```

**Windows:**
Download from [libimobiledevice for Windows](https://github.com/libimobiledevice-win32/imobiledevice-net)

### Install the library

```bash
pip install ios-control
```

Or for development:
```bash
git clone https://github.com/import1bones/ios-control.git
cd ios-control
pip install -e .
```

## Quick Start

```python
from ios_control import IOSDevice

# Connect to the first available iOS device
with IOSDevice() as device:
    print(f"Connected to: {device}")
    
    # Get device information
    info = device.get_device_info()
    print(f"Device Name: {info.get('DeviceName')}")
    print(f"iOS Version: {info.get('ProductVersion')}")
    
    # List installed apps
    apps = device.list_apps()
    print(f"Installed apps: {len(apps)}")
    
    # Take a screenshot
    device.screenshot("my_screenshot.png")
```

## API Reference

### IOSDevice Class

The main class for interacting with iOS devices.

#### Constructor

```python
IOSDevice(udid=None)
```

- `udid` (optional): Specific device UDID to connect to. If None, connects to the first available device.

#### Methods

**Connection Management:**
- `connect()` - Connect to the device
- `disconnect()` - Disconnect from the device
- `is_connected` - Property to check connection status

**Device Information:**
- `get_device_info()` - Get detailed device information
- `device_info` - Property to get basic device info

**App Management:**
- `list_apps()` - List all installed apps
- `install_app(ipa_path)` - Install an app from IPA file
- `uninstall_app(bundle_id)` - Uninstall an app by bundle ID

**Device Control:**
- `screenshot(output_path)` - Take a screenshot
- `reboot()` - Reboot the device

**UI Automation:**
- `tap(x, y)` - Tap at specific coordinates
- `tap_by_text(text, exact_match)` - Tap element containing text
- `swipe(start_x, start_y, end_x, end_y, duration)` - Swipe between points
- `long_press(x, y, duration)` - Long press at coordinates
- `input_text(text)` - Input text into focused field
- `home_button()` - Press home button
- `back_button()` - Perform back gesture
- `wait_for_element_by_text(text, timeout)` - Wait for element to appear
- `get_screen_size()` - Get device screen dimensions

**Static Methods:**
- `IOSDevice.list_devices()` - List all available iOS devices

## Examples

### Connect to a specific device

```python
from ios_control import IOSDevice

# List available devices
devices = IOSDevice.list_devices()
for device in devices:
    print(f"UDID: {device['udid']}, Name: {device['name']}")

# Connect to specific device
device = IOSDevice(udid="your-device-udid-here")
device.connect()

# Your code here...

device.disconnect()
```

### App management

```python
from ios_control import IOSDevice

with IOSDevice() as device:
    # List installed apps
    apps = device.list_apps()
    for app in apps:
        print(f"App: {app['name']} ({app['bundle_id']})")
    
    # Install an app
    device.install_app("/path/to/your/app.ipa")
    
    # Uninstall an app
    device.uninstall_app("com.example.app")
```

### UI Automation

```python
from ios_control import IOSDevice

with IOSDevice() as device:
    # Get screen size
    width, height = device.get_screen_size()
    print(f"Screen size: {width}x{height}")
    
    # Tap at coordinates
    device.tap(100, 200)
    
    # Tap on element by text
    device.tap_by_text("Settings")
    
    # Swipe (scroll down)
    device.swipe(width//2, 200, width//2, 600, duration=0.5)
    
    # Input text (into focused text field)
    device.input_text("Hello World")
    
    # Long press
    device.long_press(200, 300, duration=1.0)
    
    # Press home button
    device.home_button()
    
    # Wait for element to appear
    if device.wait_for_element_by_text("Calculator", timeout=10):
        device.tap_by_text("Calculator")
```

## Command Line Interface

The library also provides a CLI tool for easy command-line usage:

```bash
# List available devices
ios-control devices

# Get device information
ios-control info

# Take a screenshot
ios-control screenshot -o my_screenshot.png

# List installed apps
ios-control apps

# UI Automation commands
ios-control tap 100 200                    # Tap at coordinates (100, 200)
ios-control tap-text "Settings"            # Tap on element with text "Settings"
ios-control tap-text "Calculator" --exact  # Exact text match
ios-control swipe 100 200 300 400          # Swipe from (100,200) to (300,400)
ios-control input "Hello World"            # Input text
ios-control home                           # Press home button
ios-control back                           # Perform back gesture
ios-control longpress 150 250 --duration 2.0  # Long press for 2 seconds

# Use specific device by UDID
ios-control --udid YOUR-DEVICE-UDID tap 100 100
```

### Error handling

```python
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError

try:
    with IOSDevice() as device:
        device.screenshot("screenshot.png")
except DeviceNotFoundError:
    print("No iOS device found")
except IOSConnectionError as e:
    print(f"Connection error: {e}")
```

## Troubleshooting

### "No iOS devices found"
- Make sure your iOS device is connected via USB
- Ensure the device is unlocked and you've trusted the computer
- Verify `libimobiledevice` tools are installed correctly

### "libimobiledevice tools not installed"
- Install the required tools using the instructions in the Prerequisites section
- Make sure the tools are in your system PATH

### Permission issues
- On macOS, you might need to grant terminal/Python permission to access connected devices
- Try running with `sudo` if you encounter permission errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [libimobiledevice](https://libimobiledevice.org/)
- Inspired by [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)