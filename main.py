#!/usr/bin/env python3
"""
iOS Contro            print("✓ Connected successfully!")

            # Get device info
            info = device.get_device_info()
            print("\nDevice Details:")
            print(f"  Name: {info.get('DeviceName', 'Unknown')}")
            print(f"  Model: {info.get('ProductType', 'Unknown')}")
            print(f"  iOS Version: {info.get('ProductVersion', 'Unknown')}")

            # Get screen size
            width, height = device.get_screen_size()
            print(f"  Screen Size: {width}x{height}")

            print("\n✓ Demo completed successfully!")
            print("   Available examples:")
            print("   - examples/basic_example.py - Basic device operations")
            print("   - examples/app_management.py - App installation/management")
            print("   - examples/ui_automation_demo.py - UI automation features")
            print("   - Run 'ios-control --help' for CLI usage") Main Entry Point

This is a simple example of how to use the ios-control library.
For more detailed examples, see the examples/ directory.
"""

from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def main():
    """Main function demonstrating basic ios-control usage."""
    print("iOS Control Library - Quick Demo")
    print("=" * 40)

    try:
        # List available devices
        print("Scanning for iOS devices...")
        devices = IOSDevice.list_devices()

        if not devices:
            print("❌ No iOS devices found.")
            print("   Please connect an iOS device and make sure:")
            print("   - The device is unlocked")
            print("   - You've trusted this computer")
            print("   - libimobiledevice tools are installed")
            return

        print(f"✓ Found {len(devices)} device(s):")
        for device in devices:
            print(f"  • {device['name']} (iOS {device['ios_version']})")

        # Connect to first device and get basic info
        print(f"\nConnecting to {devices[0]['name']}...")

        with IOSDevice() as device:
            print("✓ Connected successfully!")

            # Get device info
            info = device.get_device_info()
            print("\nDevice Details:")
            print(f"  Name: {info.get('DeviceName', 'Unknown')}")
            print(f"  Model: {info.get('ProductType', 'Unknown')}")
            print(f"  iOS Version: {info.get('ProductVersion', 'Unknown')}")

            print("\n✓ Demo completed successfully!")
            print("   Check the examples/ directory for more advanced usage.")

    except DeviceNotFoundError as e:
        print(f"❌ Device Error: {e}")
    except IOSConnectionError as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main()
