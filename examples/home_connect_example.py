#!/usr/bin/env python3
"""
Home Connect App Automation Example

This example demonstrates how to use the ios-control library to:
1. Open the Home Connect app
2. Navigate through the app interface
3. Add a new appliance (dishwasher) to the home network

Usage:
    python examples/home_connect_example.py
"""

import time
from ios_control import IOSDevice, DeviceNotFoundError, IOSConnectionError


def open_home_connect_and_add_appliance():
    """
    Main workflow for opening Home Connect app and adding an appliance.

    This function demonstrates a complete user workflow:
    1. Connect to iOS device
    2. Navigate to home screen
    3. Open Home Connect app
    4. Add a new dishwasher appliance
    5. Configure network settings
    """
    try:
        print("🏠 Home Connect App Automation Demo")
        print("=" * 40)

        # Connect to device
        with IOSDevice() as device:
            print(f"✓ Connected to: {device}")

            # Get screen information
            width, height = device.get_screen_size()
            print(f"📱 Screen size: {width}x{height}")

            # Step 1: Go to home screen
            print("\n1️⃣ Going to home screen...")
            device.home_button()
            time.sleep(2)
            device.screenshot("01_home_screen.png")
            print("   📸 Screenshot saved: 01_home_screen.png")

            # Step 2: Look for and open Home Connect app
            print("\n2️⃣ Looking for Home Connect app...")
            if device.wait_for_element_by_text("Home Connect", timeout=10):
                print("   ✓ Found Home Connect app")
                device.tap_by_text("Home Connect")
                print("   ✓ Tapped on Home Connect app")
                time.sleep(3)  # Wait for app to load
                device.screenshot("02_app_opening.png")
            else:
                print("   ❌ Home Connect app not found on home screen")
                print("   💡 Trying to search for the app...")

                # Try using Spotlight search
                device.swipe(width // 2, 100, width // 2, height // 2, duration=0.5)
                time.sleep(1)

                if device.wait_for_element_by_text("Search", timeout=3):
                    device.tap_by_text("Search")
                    time.sleep(1)
                    device.input_text("Home Connect")
                    time.sleep(2)

                    if device.wait_for_element_by_text("Home Connect", timeout=5):
                        device.tap_by_text("Home Connect")
                        time.sleep(3)
                    else:
                        print("   ❌ Home Connect app not found in search")
                        return False
                else:
                    print("   ❌ Could not access search")
                    return False

            # Step 3: Navigate to add appliance
            print("\n3️⃣ Navigating to add appliance...")
            device.screenshot("03_app_loaded.png")

            # Look for various possible buttons to add appliances
            add_buttons = ["Add Appliance", "Add Device", "+", "Add", "New Appliance"]
            button_found = False

            for button_text in add_buttons:
                if device.wait_for_element_by_text(button_text, timeout=3):
                    print(f"   ✓ Found '{button_text}' button")
                    device.tap_by_text(button_text)
                    button_found = True
                    break

            if not button_found:
                print("   ⚠️  Add button not found, trying coordinate tap...")
                # Try tapping in common locations for add buttons
                device.tap(width - 50, 100)  # Top right corner
                time.sleep(1)

            time.sleep(2)
            device.screenshot("04_add_appliance_screen.png")

            # Step 4: Select appliance type (Dishwasher)
            print("\n4️⃣ Selecting appliance type...")

            appliance_types = ["Dishwasher", "Dish Washer", "Dishwashers"]
            appliance_found = False

            for appliance in appliance_types:
                if device.wait_for_element_by_text(appliance, timeout=5):
                    print(f"   ✓ Found '{appliance}' option")
                    device.tap_by_text(appliance)
                    appliance_found = True
                    break

            if not appliance_found:
                print("   ⚠️  Dishwasher option not visible, scrolling down...")
                device.swipe(
                    width // 2, height * 0.7, width // 2, height * 0.3, duration=0.5
                )
                time.sleep(1)

                # Try again after scrolling
                for appliance in appliance_types:
                    if device.wait_for_element_by_text(appliance, timeout=3):
                        print(f"   ✓ Found '{appliance}' after scrolling")
                        device.tap_by_text(appliance)
                        appliance_found = True
                        break

            if not appliance_found:
                print("   ❌ Could not find dishwasher option")
                # Continue anyway for demonstration

            time.sleep(2)
            device.screenshot("05_appliance_selected.png")

            # Step 5: Network setup (if required)
            print("\n5️⃣ Setting up network connection...")

            # Look for network-related fields
            network_fields = ["Network", "WiFi", "Wi-Fi", "SSID", "Network Name"]

            for field in network_fields:
                if device.wait_for_element_by_text(field, timeout=3):
                    print(f"   ✓ Found network field: '{field}'")
                    device.tap_by_text(field)
                    time.sleep(1)
                    device.input_text("MyHomeWiFi")
                    print("   ✓ Entered network name")
                    break

            # Look for password field
            password_fields = ["Password", "Pass", "Key", "Security Key"]

            for field in password_fields:
                if device.wait_for_element_by_text(field, timeout=3):
                    print(f"   ✓ Found password field: '{field}'")
                    device.tap_by_text(field)
                    time.sleep(1)
                    device.input_text("MySecurePassword123")
                    print("   ✓ Entered password")
                    break

            device.screenshot("06_network_configured.png")

            # Step 6: Connect/Complete setup
            print("\n6️⃣ Completing appliance setup...")

            # Look for connection/completion buttons
            connect_buttons = ["Connect", "Add", "Continue", "Next", "Done", "Finish"]

            for button in connect_buttons:
                if device.wait_for_element_by_text(button, timeout=3):
                    print(f"   ✓ Found '{button}' button")
                    device.tap_by_text(button)
                    print(f"   ✓ Tapped '{button}'")
                    time.sleep(3)  # Wait for connection process
                    break

            # Final screenshot
            device.screenshot("07_setup_complete.png")

            print("\n✅ Home Connect appliance setup workflow completed!")
            print("📸 Screenshots saved:")
            print("   - 01_home_screen.png")
            print("   - 02_app_opening.png")
            print("   - 03_app_loaded.png")
            print("   - 04_add_appliance_screen.png")
            print("   - 05_appliance_selected.png")
            print("   - 06_network_configured.png")
            print("   - 07_setup_complete.png")

            return True

    except DeviceNotFoundError:
        print("❌ No iOS device found. Please connect a device and try again.")
        return False
    except IOSConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def demo_coordinate_based_approach():
    """
    Alternative approach using coordinate-based tapping.

    This method is useful when text-based element detection fails
    or when you know the exact positions of UI elements.
    """
    try:
        print("\n🎯 Coordinate-based Home Connect Demo")
        print("=" * 40)

        with IOSDevice() as device:
            print(f"✓ Connected to: {device}")
            width, height = device.get_screen_size()
            print(f"📱 Screen size: {width}x{height}")

            # Go to home screen
            device.home_button()
            time.sleep(2)

            # Known coordinates for Home Connect app (example for iPhone)
            # These coordinates would need to be adjusted based on actual device/layout
            if width == 375:  # iPhone standard size
                home_connect_x, home_connect_y = 187, 200  # Center of app icon
                add_button_x, add_button_y = 320, 120  # Top-right add button
                dishwasher_x, dishwasher_y = 187, 300  # Dishwasher option
                connect_x, connect_y = 187, 500  # Connect button
            else:  # Adjust for other screen sizes
                home_connect_x = width // 4
                home_connect_y = height // 4
                add_button_x = width - 50
                add_button_y = 120
                dishwasher_x = width // 2
                dishwasher_y = height // 2
                connect_x = width // 2
                connect_y = height * 0.75

            print("\n📍 Using coordinate-based navigation:")

            # Tap Home Connect app
            print(f"   Tapping Home Connect at ({home_connect_x}, {home_connect_y})")
            device.tap(home_connect_x, home_connect_y)
            time.sleep(3)

            # Tap add button
            print(f"   Tapping Add button at ({add_button_x}, {add_button_y})")
            device.tap(add_button_x, add_button_y)
            time.sleep(2)

            # Tap dishwasher option
            print(f"   Tapping Dishwasher at ({dishwasher_x}, {dishwasher_y})")
            device.tap(dishwasher_x, dishwasher_y)
            time.sleep(2)

            # Enter network information (assuming text fields are active)
            print("   Entering network credentials...")
            device.input_text("MyHomeNetwork")
            time.sleep(1)
            device.input_text("MyPassword123")
            time.sleep(1)

            # Tap connect button
            print(f"   Tapping Connect at ({connect_x}, {connect_y})")
            device.tap(connect_x, connect_y)
            time.sleep(3)

            device.screenshot("coordinate_demo_complete.png")
            print("✅ Coordinate-based demo completed!")

            return True

    except Exception as e:
        print(f"❌ Error in coordinate demo: {e}")
        return False


def interactive_home_connect_demo():
    """
    Interactive demo allowing manual control of the Home Connect workflow.
    """
    print("\n🎮 Interactive Home Connect Demo")
    print("=" * 40)
    print("Commands:")
    print("  home     - Go to home screen")
    print("  open     - Open Home Connect app")
    print("  add      - Tap add appliance")
    print("  dish     - Select dishwasher")
    print("  network  - Enter network info")
    print("  connect  - Connect appliance")
    print("  shot     - Take screenshot")
    print("  auto     - Run automatic workflow")
    print("  quit     - Exit")

    try:
        with IOSDevice() as device:
            print(f"\n✓ Connected to: {device}")

            while True:
                command = input("\n> ").strip().lower()

                if command == "quit":
                    break
                elif command == "home":
                    device.home_button()
                    print("✓ Went to home screen")
                elif command == "open":
                    if device.tap_by_text("Home Connect"):
                        print("✓ Opened Home Connect")
                    else:
                        print("❌ Home Connect not found")
                elif command == "add":
                    if device.tap_by_text("Add Appliance"):
                        print("✓ Tapped Add Appliance")
                    else:
                        print("❌ Add button not found")
                elif command == "dish":
                    if device.tap_by_text("Dishwasher"):
                        print("✓ Selected Dishwasher")
                    else:
                        print("❌ Dishwasher option not found")
                elif command == "network":
                    device.input_text("MyWiFiNetwork")
                    print("✓ Entered network name")
                elif command == "connect":
                    if device.tap_by_text("Connect"):
                        print("✓ Tapped Connect")
                    else:
                        print("❌ Connect button not found")
                elif command == "shot":
                    filename = f"interactive_{int(time.time())}.png"
                    device.screenshot(filename)
                    print(f"✓ Screenshot saved: {filename}")
                elif command == "auto":
                    print("Running automatic workflow...")
                    open_home_connect_and_add_appliance()
                else:
                    print("❌ Unknown command")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to choose demo type."""
    print("Home Connect App Automation")
    print("=" * 30)
    print("Choose demo type:")
    print("1. Automatic text-based workflow")
    print("2. Coordinate-based approach")
    print("3. Interactive mode")

    try:
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            success = open_home_connect_and_add_appliance()
            if success:
                print("\n🎉 Automatic workflow completed successfully!")
            else:
                print("\n⚠️  Workflow encountered issues")
        elif choice == "2":
            success = demo_coordinate_based_approach()
            if success:
                print("\n🎉 Coordinate demo completed!")
        elif choice == "3":
            interactive_home_connect_demo()
        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
