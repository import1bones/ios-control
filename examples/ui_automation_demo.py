#!/usr/bin/env python3
"""
UI Automation Example

This example demonstrates the UI automation capabilities of the ios-control library,
including tapping, swiping, text input, and element interaction.
"""

import time
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def demo_basic_interactions():
    """Demonstrate basic tap and swipe interactions."""
    print("=== Basic UI Interactions Demo ===")

    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")

            # Get screen size
            width, height = device.get_screen_size()
            print(f"Screen size: {width}x{height}")

            # Take initial screenshot
            device.screenshot("before_demo.png")
            print("📸 Initial screenshot saved")

            # Demo 1: Tap at center of screen
            print("\n1. Tapping at center of screen...")
            center_x, center_y = width // 2, height // 2
            device.tap(center_x, center_y)
            time.sleep(1)

            # Demo 2: Swipe up (scroll up)
            print("2. Swiping up (scroll up)...")
            device.swipe(center_x, height - 100, center_x, 100, duration=0.5)
            time.sleep(1)

            # Demo 3: Swipe down (scroll down)
            print("3. Swiping down (scroll down)...")
            device.swipe(center_x, 100, center_x, height - 100, duration=0.5)
            time.sleep(1)

            # Demo 4: Swipe left (navigate)
            print("4. Swiping left...")
            device.swipe(width - 50, center_y, 50, center_y, duration=0.3)
            time.sleep(1)

            # Demo 5: Home button
            print("5. Pressing home button...")
            device.home_button()
            time.sleep(2)

            # Take final screenshot
            device.screenshot("after_demo.png")
            print("📸 Final screenshot saved")

    except DeviceNotFoundError:
        print("❌ No iOS device found")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")


def demo_text_interaction():
    """Demonstrate text-based interactions."""
    print("\n=== Text-based Interactions Demo ===")

    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")

            # Demo 1: Try to find and tap Settings app
            print("1. Looking for 'Settings' app...")
            if device.wait_for_element_by_text("Settings", timeout=5):
                print("   Found Settings app, tapping...")
                device.tap_by_text("Settings")
                time.sleep(2)

                # Demo 2: Look for General settings
                print("2. Looking for 'General' in settings...")
                if device.wait_for_element_by_text("General", timeout=5):
                    print("   Found General, tapping...")
                    device.tap_by_text("General")
                    time.sleep(2)

                    # Demo 3: Go back using back gesture
                    print("3. Going back...")
                    device.back_button()
                    time.sleep(1)

                # Demo 4: Go to home
                print("4. Going to home...")
                device.home_button()
                time.sleep(1)
            else:
                print("   Settings app not found on current screen")

    except DeviceNotFoundError:
        print("❌ No iOS device found")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")


def demo_text_input():
    """Demonstrate text input functionality."""
    print("\n=== Text Input Demo ===")

    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")

            # Try to open Spotlight search (swipe down from top)
            print("1. Opening Spotlight search...")
            width, height = device.get_screen_size()
            device.swipe(width // 2, 50, width // 2, height // 2, duration=0.5)
            time.sleep(1)

            # Wait for search field and input text
            print("2. Waiting for search field...")
            if device.wait_for_element_by_text("Search", timeout=3, exact_match=False):
                print("3. Found search field, tapping...")
                device.tap_by_text("Search", exact_match=False)
                time.sleep(1)

                print("4. Typing 'Calculator'...")
                device.input_text("Calculator")
                time.sleep(1)

                # Try to tap on Calculator result
                print("5. Looking for Calculator app...")
                if device.wait_for_element_by_text("Calculator", timeout=3):
                    print("   Found Calculator, tapping...")
                    device.tap_by_text("Calculator")
                    time.sleep(2)

                    # Go back to home
                    print("6. Going back to home...")
                    device.home_button()
                    time.sleep(1)
            else:
                print("   Search field not found")

    except DeviceNotFoundError:
        print("❌ No iOS device found")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")


def demo_long_press():
    """Demonstrate long press functionality."""
    print("\n=== Long Press Demo ===")

    try:
        with IOSDevice() as device:
            print(f"Connected to: {device}")

            # Get screen dimensions
            width, height = device.get_screen_size()

            print("1. Long pressing at center of screen...")
            device.long_press(width // 2, height // 2, duration=1.5)
            time.sleep(2)

            # Tap somewhere else to dismiss any context menu
            print("2. Tapping elsewhere to dismiss...")
            device.tap(100, 100)
            time.sleep(1)

    except DeviceNotFoundError:
        print("❌ No iOS device found")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")


def interactive_mode():
    """Interactive mode for manual testing."""
    print("\n=== Interactive Mode ===")
    print("Commands:")
    print("  tap <x> <y>         - Tap at coordinates")
    print("  text <message>      - Input text")
    print("  tap_text <text>     - Tap element with text")
    print("  swipe <x1> <y1> <x2> <y2> - Swipe from point to point")
    print("  home                - Press home button")
    print("  back                - Back gesture")
    print("  screenshot <name>   - Take screenshot")
    print("  screen              - Show screen size")
    print("  quit                - Exit interactive mode")

    try:
        with IOSDevice() as device:
            print(f"\nConnected to: {device}")
            width, height = device.get_screen_size()
            print(f"Screen size: {width}x{height}")

            while True:
                try:
                    command = input("\n> ").strip().split()
                    if not command:
                        continue

                    cmd = command[0].lower()

                    if cmd == "quit":
                        break
                    elif cmd == "tap" and len(command) == 3:
                        x, y = int(command[1]), int(command[2])
                        device.tap(x, y)
                        print(f"✓ Tapped at ({x}, {y})")
                    elif cmd == "text" and len(command) >= 2:
                        text = " ".join(command[1:])
                        device.input_text(text)
                        print(f"✓ Typed: {text}")
                    elif cmd == "tap_text" and len(command) >= 2:
                        text = " ".join(command[1:])
                        if device.tap_by_text(text):
                            print(f"✓ Tapped element with text: {text}")
                        else:
                            print(f"❌ Element with text '{text}' not found")
                    elif cmd == "swipe" and len(command) == 5:
                        x1, y1, x2, y2 = map(int, command[1:5])
                        device.swipe(x1, y1, x2, y2)
                        print(f"✓ Swiped from ({x1}, {y1}) to ({x2}, {y2})")
                    elif cmd == "home":
                        device.home_button()
                        print("✓ Pressed home button")
                    elif cmd == "back":
                        device.back_button()
                        print("✓ Performed back gesture")
                    elif cmd == "screenshot":
                        name = (
                            command[1]
                            if len(command) > 1
                            else "interactive_screenshot.png"
                        )
                        device.screenshot(name)
                        print(f"✓ Screenshot saved: {name}")
                    elif cmd == "screen":
                        print(f"Screen size: {width}x{height}")
                    else:
                        print("❌ Invalid command or wrong number of arguments")

                except ValueError:
                    print("❌ Invalid coordinates (must be numbers)")
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")

    except DeviceNotFoundError:
        print("❌ No iOS device found")
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")


def main():
    """Main function to run all demos."""
    print("iOS Control - UI Automation Demo")
    print("=" * 40)

    print("\nAvailable demos:")
    print("1. Basic interactions (tap, swipe, home)")
    print("2. Text-based interactions (tap by text)")
    print("3. Text input demo")
    print("4. Long press demo")
    print("5. Interactive mode")
    print("6. Run all demos")

    try:
        choice = input("\nSelect demo (1-6): ").strip()

        if choice == "1":
            demo_basic_interactions()
        elif choice == "2":
            demo_text_interaction()
        elif choice == "3":
            demo_text_input()
        elif choice == "4":
            demo_long_press()
        elif choice == "5":
            interactive_mode()
        elif choice == "6":
            demo_basic_interactions()
            demo_text_interaction()
            demo_text_input()
            demo_long_press()
        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}")


if __name__ == "__main__":
    main()
