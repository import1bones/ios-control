#!/usr/bin/env python3
"""
App Management Example

This example demonstrates how to manage apps on iOS devices.
"""

import sys
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def list_apps_example():
    """List all installed apps on the device."""
    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")

            apps = device.list_apps()
            print(f"\nFound {len(apps)} installed apps:")

            for i, app in enumerate(apps, 1):
                print(f"{i:3d}. {app['name']}")
                print(f"     Bundle ID: {app['bundle_id']}")
                print()

    except DeviceNotFoundError:
        print("No iOS devices found. Please connect a device.")
    except IOSConnectionError as e:
        print(f"Connection error: {e}")


def install_app_example(ipa_path):
    """Install an app from IPA file."""
    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")
            print(f"Installing app from: {ipa_path}")

            success = device.install_app(ipa_path)
            if success:
                print("✓ App installed successfully!")
            else:
                print("❌ App installation failed.")

    except DeviceNotFoundError:
        print("No iOS devices found. Please connect a device.")
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
    except FileNotFoundError:
        print(f"IPA file not found: {ipa_path}")


def uninstall_app_example(bundle_id):
    """Uninstall an app by bundle ID."""
    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")
            print(f"Uninstalling app: {bundle_id}")

            success = device.uninstall_app(bundle_id)
            if success:
                print("✓ App uninstalled successfully!")
            else:
                print("❌ App uninstallation failed.")

    except DeviceNotFoundError:
        print("No iOS devices found. Please connect a device.")
    except IOSConnectionError as e:
        print(f"Connection error: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python app_management.py list")
        print("  python app_management.py install <path_to_ipa>")
        print("  python app_management.py uninstall <bundle_id>")
        return

    command = sys.argv[1]

    if command == "list":
        list_apps_example()
    elif command == "install":
        if len(sys.argv) < 3:
            print("Please provide the path to the IPA file.")
            return
        install_app_example(sys.argv[2])
    elif command == "uninstall":
        if len(sys.argv) < 3:
            print("Please provide the bundle ID of the app to uninstall.")
            return
        uninstall_app_example(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print("Available commands: list, install, uninstall")


if __name__ == "__main__":
    main()
