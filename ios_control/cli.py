#!/usr/bin/env python3
"""
iOS Control CLI - Command Line Interface

A simple command-line interface for the ios-control library.
"""

import argparse
import sys
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def cmd_list_devices():
    """List all available iOS devices."""
    devices = IOSDevice.list_devices()

    if not devices:
        print("No iOS devices found.")
        return False

    print(f"Found {len(devices)} device(s):")
    for i, device in enumerate(devices, 1):
        print(f"  {i}. {device['name']}")
        print(f"     UDID: {device['udid']}")
        print(f"     iOS Version: {device['ios_version']}")
        print()

    return True


def cmd_device_info(udid=None):
    """Show detailed device information."""
    try:
        with IOSDevice(udid=udid) as device:
            info = device.get_device_info()

            print("Device Information:")
            print("-" * 30)
            for key, value in sorted(info.items()):
                print(f"{key}: {value}")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_screenshot(udid=None, output="screenshot.png"):
    """Take a screenshot of the device."""
    try:
        with IOSDevice(udid=udid) as device:
            path = device.screenshot(output)
            print(f"Screenshot saved to: {path}")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_list_apps(udid=None):
    """List installed apps on the device."""
    try:
        with IOSDevice(udid=udid) as device:
            apps = device.list_apps()

            print(f"Found {len(apps)} installed apps:")
            for app in apps:
                print(f"  • {app['name']} ({app['bundle_id']})")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_tap(udid=None, x=0, y=0):
    """Tap at specified coordinates."""
    try:
        with IOSDevice(udid=udid) as device:
            device.tap(x, y)
            print(f"Tapped at ({x}, {y})")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_tap_text(udid=None, text="", exact=False):
    """Tap element by text."""
    try:
        with IOSDevice(udid=udid) as device:
            if device.tap_by_text(text, exact_match=exact):
                match_type = "exact" if exact else "partial"
                print(f"Tapped element with text '{text}' ({match_type} match)")
            else:
                print(f"Element with text '{text}' not found")
                return False

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_swipe(udid=None, x1=0, y1=0, x2=0, y2=0, duration=0.5):
    """Swipe between coordinates."""
    try:
        with IOSDevice(udid=udid) as device:
            device.swipe(x1, y1, x2, y2, duration)
            print(f"Swiped from ({x1}, {y1}) to ({x2}, {y2}) in {duration}s")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_input_text(udid=None, text=""):
    """Input text on device."""
    try:
        with IOSDevice(udid=udid) as device:
            device.input_text(text)
            print(f"Input text: {text}")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_home_button(udid=None):
    """Press home button."""
    try:
        with IOSDevice(udid=udid) as device:
            device.home_button()
            print("Pressed home button")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_back_button(udid=None):
    """Perform back gesture."""
    try:
        with IOSDevice(udid=udid) as device:
            device.back_button()
            print("Performed back gesture")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def cmd_long_press(udid=None, x=0, y=0, duration=1.0):
    """Long press at coordinates."""
    try:
        with IOSDevice(udid=udid) as device:
            device.long_press(x, y, duration)
            print(f"Long pressed at ({x}, {y}) for {duration}s")

    except DeviceNotFoundError:
        print("No iOS device found.")
        return False
    except IOSConnectionError as e:
        print(f"Connection error: {e}")
        return False

    return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="iOS Control CLI - Control iOS devices from command line"
    )
    parser.add_argument("--udid", help="Specific device UDID to use")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List devices command
    subparsers.add_parser("devices", help="List all available iOS devices")

    # Device info command
    subparsers.add_parser("info", help="Show detailed device information")

    # Screenshot command
    screenshot_parser = subparsers.add_parser("screenshot", help="Take a screenshot")
    screenshot_parser.add_argument(
        "-o",
        "--output",
        default="screenshot.png",
        help="Output file path (default: screenshot.png)",
    )

    # List apps command
    subparsers.add_parser("apps", help="List installed apps")

    # UI Automation commands
    tap_parser = subparsers.add_parser("tap", help="Tap at coordinates")
    tap_parser.add_argument("x", type=int, help="X coordinate")
    tap_parser.add_argument("y", type=int, help="Y coordinate")

    tap_text_parser = subparsers.add_parser("tap-text", help="Tap element by text")
    tap_text_parser.add_argument("text", help="Text to search for")
    tap_text_parser.add_argument(
        "--exact", action="store_true", help="Exact text match"
    )

    swipe_parser = subparsers.add_parser("swipe", help="Swipe between coordinates")
    swipe_parser.add_argument("x1", type=int, help="Start X coordinate")
    swipe_parser.add_argument("y1", type=int, help="Start Y coordinate")
    swipe_parser.add_argument("x2", type=int, help="End X coordinate")
    swipe_parser.add_argument("y2", type=int, help="End Y coordinate")
    swipe_parser.add_argument(
        "--duration", type=float, default=0.5, help="Swipe duration in seconds"
    )

    input_parser = subparsers.add_parser("input", help="Input text")
    input_parser.add_argument("text", help="Text to input")

    subparsers.add_parser("home", help="Press home button")
    subparsers.add_parser("back", help="Perform back gesture")

    longpress_parser = subparsers.add_parser(
        "longpress", help="Long press at coordinates"
    )
    longpress_parser.add_argument("x", type=int, help="X coordinate")
    longpress_parser.add_argument("y", type=int, help="Y coordinate")
    longpress_parser.add_argument(
        "--duration", type=float, default=1.0, help="Press duration in seconds"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    success = False

    if args.command == "devices":
        success = cmd_list_devices()
    elif args.command == "info":
        success = cmd_device_info(args.udid)
    elif args.command == "screenshot":
        success = cmd_screenshot(args.udid, args.output)
    elif args.command == "apps":
        success = cmd_list_apps(args.udid)
    elif args.command == "tap":
        success = cmd_tap(args.udid, args.x, args.y)
    elif args.command == "tap-text":
        success = cmd_tap_text(args.udid, args.text, args.exact)
    elif args.command == "swipe":
        success = cmd_swipe(
            args.udid, args.x1, args.y1, args.x2, args.y2, args.duration
        )
    elif args.command == "input":
        success = cmd_input_text(args.udid, args.text)
    elif args.command == "home":
        success = cmd_home_button(args.udid)
    elif args.command == "back":
        success = cmd_back_button(args.udid)
    elif args.command == "longpress":
        success = cmd_long_press(args.udid, args.x, args.y, args.duration)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
