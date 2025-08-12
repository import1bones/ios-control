#!/usr/bin/env python3
"""
Basic iOS Control Example

This example demonstrates basic usage of the ios-control library.
"""

from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def main():
    try:
        # List all available devices
        print("Scanning for iOS devices...")
        devices = IOSDevice.list_devices()

        if not devices:
            print("No iOS devices found. Please connect a device and try again.")
            return

        print(f"Found {len(devices)} device(s):")
        for i, device in enumerate(devices):
            print(
                f"  {i + 1}. {device['name']} (UDID: {device['udid']}) - iOS {device['ios_version']}"
            )

        # Connect to the first device
        print(f"\nConnecting to {devices[0]['name']}...")

        with IOSDevice(udid=devices[0]["udid"]) as device:
            print(f"✓ Connected to {device}")

            # Get detailed device information
            print("\n--- Device Information ---")
            info = device.get_device_info()
            print(f"Device Name: {info.get('DeviceName', 'Unknown')}")
            print(f"Product Type: {info.get('ProductType', 'Unknown')}")
            print(f"iOS Version: {info.get('ProductVersion', 'Unknown')}")
            print(f"Serial Number: {info.get('SerialNumber', 'Unknown')}")
            print(f"WiFi Address: {info.get('WiFiAddress', 'Unknown')}")

            # List installed apps
            print("\n--- Installed Apps ---")
            try:
                apps = device.list_apps()
                print(f"Found {len(apps)} installed apps:")
                for app in apps[:10]:  # Show first 10 apps
                    print(f"  • {app['name']} ({app['bundle_id']})")
                if len(apps) > 10:
                    print(f"  ... and {len(apps) - 10} more apps")
            except Exception as e:
                print(f"Could not list apps: {e}")

            # Take a screenshot
            print("\n--- Taking Screenshot ---")
            try:
                screenshot_path = device.screenshot("device_screenshot.png")
                print(f"✓ Screenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"Could not take screenshot: {e}")

    except DeviceNotFoundError:
        print("❌ No iOS devices found. Please connect a device and try again.")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
