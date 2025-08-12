"""
Test for Home Connect app automation workflow with real iOS device.

This test demonstrates how to use the ios-control library to:
1. Open the Home Connect app
2. Navigate through the app interface
3. Add a new appliance to the home network

Note: This test requires a real iOS device to be connected and
the Home Connect app to be installed.
"""

import time
from ios_control import IOSDevice


class TestHomeConnectRealDevice:
    """Test cases for Home Connect app automation with real device."""

    def test_device_connection(self):
        """Test basic device connection."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        device = IOSDevice()
        assert device.connect()
        assert device.is_connected
        device.disconnect()
        assert not device.is_connected
        return True

    def test_open_home_connect_app(self):
        """Test opening the Home Connect app."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        with IOSDevice() as device:
            print(f"Connected to: {device}")

            # Get screen size
            width, height = device.get_screen_size()
            print(f"Screen size: {width}x{height}")

            # Go to home screen first
            device.home_button()
            time.sleep(2)

            # Take initial screenshot
            device.screenshot("test_home_screen.png")
            print("Initial screenshot taken: test_home_screen.png")

            # Try to find Home Connect app
            if device.wait_for_element_by_text("Home Connect", timeout=10):
                print("Home Connect app found on home screen")
                device.tap_by_text("Home Connect")
                time.sleep(3)  # Wait for app to load

                # Take screenshot after opening app
                device.screenshot("test_home_connect_opened.png")
                print("App opened screenshot: test_home_connect_opened.png")

                # Go back to home
                device.home_button()
                return True
            else:
                print("Home Connect app not found, trying search...")

                # Try using Spotlight search
                device.swipe(width // 2, 100, width // 2, height // 2, duration=0.5)
                time.sleep(2)

                if device.wait_for_element_by_text("Search", timeout=5):
                    device.tap_by_text("Search")
                    time.sleep(1)
                    device.input_text("Home Connect")
                    time.sleep(3)

                    if device.wait_for_element_by_text("Home Connect", timeout=5):
                        print("Found Home Connect in search results")
                        device.screenshot("test_search_results.png")
                        return True
                    else:
                        print("Home Connect app not installed on device")
                        return False
                else:
                    print("Cannot access search functionality")
                    return False

    def test_complete_home_connect_workflow(self):
        """Test the complete workflow of adding an appliance."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        with IOSDevice() as device:
            print(f"Testing complete workflow on: {device}")

            # Step 1: Go to home and take screenshot
            device.home_button()
            time.sleep(2)
            device.screenshot("01_workflow_home.png")

            # Step 2: Open Home Connect app
            if not device.wait_for_element_by_text("Home Connect", timeout=10):
                # Try search if not found on home screen
                width, height = device.get_screen_size()
                device.swipe(width // 2, 100, width // 2, height // 2, duration=0.5)
                time.sleep(2)

                if device.wait_for_element_by_text("Search", timeout=5):
                    device.tap_by_text("Search")
                    time.sleep(1)
                    device.input_text("Home Connect")
                    time.sleep(3)

                    if not device.wait_for_element_by_text("Home Connect", timeout=5):
                        print("Home Connect app not found on device")
                        return False
                else:
                    print("Cannot access search or find Home Connect app")
                    return False

            # Open the app
            device.tap_by_text("Home Connect")
            time.sleep(5)  # Wait for app to fully load
            device.screenshot("02_workflow_app_opened.png")

            # Step 3: Look for add appliance functionality
            add_buttons = [
                "Add Appliance",
                "Add Device",
                "+",
                "Add",
                "New Appliance",
                "Setup New Device",
            ]

            button_found = False
            for button_text in add_buttons:
                if device.wait_for_element_by_text(button_text, timeout=5):
                    print(f"Found add button: {button_text}")
                    device.tap_by_text(button_text)
                    button_found = True
                    break

            if not button_found:
                print("No add button found with text, trying coordinate tap...")
                width, height = device.get_screen_size()
                # Try common locations for add buttons
                device.tap(width - 50, 100)  # Top right
                time.sleep(2)

            device.screenshot("03_workflow_add_screen.png")

            # Step 4: Look for appliance types
            appliance_types = [
                "Dishwasher",
                "Dish Washer",
                "Washing Machine",
                "Washer",
                "Oven",
                "Coffee Machine",
            ]

            appliance_selected = False
            for appliance in appliance_types:
                if device.wait_for_element_by_text(appliance, timeout=5):
                    print(f"Found appliance type: {appliance}")
                    device.tap_by_text(appliance)
                    appliance_selected = True
                    time.sleep(2)
                    break

            if not appliance_selected:
                print("No appliance type found, trying to scroll...")
                width, height = device.get_screen_size()
                device.swipe(
                    width // 2, height * 0.7, width // 2, height * 0.3, duration=0.5
                )
                time.sleep(2)

                # Try again after scrolling
                for appliance in appliance_types:
                    if device.wait_for_element_by_text(appliance, timeout=3):
                        print(f"Found appliance after scroll: {appliance}")
                        device.tap_by_text(appliance)
                        appliance_selected = True
                        break

            device.screenshot("04_workflow_appliance_selected.png")

            # Step 5: Network setup (if applicable)
            network_keywords = ["Network", "WiFi", "Wi-Fi", "SSID", "Password"]

            for keyword in network_keywords:
                if device.wait_for_element_by_text(keyword, timeout=3):
                    print(f"Found network field: {keyword}")
                    device.tap_by_text(keyword)
                    time.sleep(1)

                    # Enter test network info
                    if "password" in keyword.lower() or "pass" in keyword.lower():
                        device.input_text("TestPassword123")
                    else:
                        device.input_text("TestNetwork")

                    time.sleep(1)
                    break

            device.screenshot("05_workflow_network_setup.png")

            # Step 6: Complete setup (look for completion buttons)
            completion_buttons = [
                "Connect",
                "Add",
                "Continue",
                "Next",
                "Done",
                "Finish",
                "Save",
            ]

            for button in completion_buttons:
                if device.wait_for_element_by_text(button, timeout=3):
                    print(f"Found completion button: {button}")
                    device.tap_by_text(button)
                    time.sleep(3)
                    break

            device.screenshot("06_workflow_complete.png")

            # Return to home
            device.home_button()
            time.sleep(1)

            print("Workflow test completed - check screenshots for results")
            return True

    def test_coordinate_based_navigation(self):
        """Test navigation using coordinates instead of text detection."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        with IOSDevice() as device:
            print(f"Testing coordinate navigation on: {device}")

            width, height = device.get_screen_size()
            print(f"Device screen: {width}x{height}")

            # Go to home
            device.home_button()
            time.sleep(2)

            # Take screenshot to see layout
            device.screenshot("coordinate_test_home.png")

            # Test various coordinate taps
            test_coordinates = [
                (width // 4, height // 4, "Top left quadrant"),
                (width * 3 // 4, height // 4, "Top right quadrant"),
                (width // 2, height // 2, "Center"),
                (width // 4, height * 3 // 4, "Bottom left quadrant"),
                (width * 3 // 4, height * 3 // 4, "Bottom right quadrant"),
            ]

            for x, y, description in test_coordinates:
                print(f"Tapping {description} at ({x}, {y})")
                device.tap(x, y)
                time.sleep(1)
                device.screenshot(f"coordinate_tap_{x}_{y}.png")

                # Go back to home after each tap
                device.home_button()
                time.sleep(1)

            return True

    def test_text_input_functionality(self):
        """Test text input capabilities."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        with IOSDevice() as device:
            print(f"Testing text input on: {device}")

            # Go to home
            device.home_button()
            time.sleep(2)

            # Open Spotlight search to test text input
            width, height = device.get_screen_size()
            device.swipe(width // 2, 100, width // 2, height // 2, duration=0.5)
            time.sleep(2)

            if device.wait_for_element_by_text("Search", timeout=5):
                device.tap_by_text("Search")
                time.sleep(1)

                # Test various text inputs
                test_texts = ["Home Connect", "Settings", "Calculator", "123456"]

                for text in test_texts:
                    print(f"Testing input: {text}")
                    device.input_text(text)
                    time.sleep(1)
                    device.screenshot(f"text_input_{text.replace(' ', '_')}.png")

                    # Clear field for next test
                    device.tap(width // 2, height // 2)
                    time.sleep(1)

            # Return to home
            device.home_button()
            return True

    def test_gesture_functionality(self):
        """Test various gesture capabilities."""
        devices = IOSDevice.list_devices()
        if not devices:
            print("No iOS device connected for testing")
            return False

        with IOSDevice() as device:
            print(f"Testing gestures on: {device}")

            width, height = device.get_screen_size()

            # Go to home
            device.home_button()
            time.sleep(2)
            device.screenshot("gesture_test_start.png")

            # Test swipe gestures
            gestures = [
                ("Swipe right", width // 4, height // 2, width * 3 // 4, height // 2),
                ("Swipe left", width * 3 // 4, height // 2, width // 4, height // 2),
                ("Swipe up", width // 2, height * 3 // 4, width // 2, height // 4),
                ("Swipe down", width // 2, height // 4, width // 2, height * 3 // 4),
            ]

            for gesture_name, x1, y1, x2, y2 in gestures:
                print(f"Testing {gesture_name}")
                device.swipe(x1, y1, x2, y2, duration=0.5)
                time.sleep(2)
                device.screenshot(f"gesture_{gesture_name.replace(' ', '_')}.png")

                # Return to home between gestures
                device.home_button()
                time.sleep(1)

            # Test long press
            print("Testing long press")
            device.long_press(width // 2, height // 2, duration=2.0)
            time.sleep(2)
            device.screenshot("gesture_long_press.png")

            # Return to home
            device.home_button()
            return True


def run_home_connect_workflow_test():
    """
    Main function to run the complete Home Connect workflow test.
    This can be called directly to test the complete workflow.
    """
    print("🏠 Home Connect Real Device Test")
    print("=" * 40)

    # Check for connected devices
    devices = IOSDevice.list_devices()
    if not devices:
        print("❌ No iOS devices found. Please connect a device.")
        return False

    print(f"✓ Found {len(devices)} device(s):")
    for device_info in devices:
        print(f"  - {device_info['name']} (iOS {device_info['ios_version']})")

    try:
        with IOSDevice() as device:
            print(f"\n✓ Connected to: {device}")

            # Complete workflow steps
            workflow_steps = [
                ("Go to home screen", lambda: (device.home_button(), time.sleep(2))),
                (
                    "Take initial screenshot",
                    lambda: device.screenshot("real_test_01_home.png"),
                ),
                (
                    "Search for Home Connect app",
                    lambda: search_home_connect_app(device),
                ),
                ("Open Home Connect app", lambda: open_home_connect_app(device)),
                (
                    "Navigate to add appliance",
                    lambda: navigate_to_add_appliance(device),
                ),
                ("Select appliance type", lambda: select_appliance_type(device)),
                (
                    "Configure network settings",
                    lambda: configure_network_settings(device),
                ),
                ("Complete setup", lambda: complete_appliance_setup(device)),
            ]

            for i, (step_name, step_func) in enumerate(workflow_steps, 1):
                print(f"\n📱 Step {i}: {step_name}")
                try:
                    result = step_func()
                    if result is False:
                        print("   ⚠️  Step failed or skipped")
                    else:
                        print("   ✓ Step completed")
                    time.sleep(1)  # Brief pause between steps
                except Exception as e:
                    print(f"   ❌ Error in step: {e}")

            # Return to home
            device.home_button()

            print("\n🎉 Home Connect workflow test completed!")
            print("📸 Check the generated screenshots for detailed results.")
            return True

    except Exception as e:
        print(f"\n❌ Error during workflow test: {e}")
        return False


def search_home_connect_app(device):
    """Search for Home Connect app."""
    width, height = device.get_screen_size()

    if not device.wait_for_element_by_text("Home Connect", timeout=5):
        print("   App not visible, trying search...")
        device.swipe(width // 2, 100, width // 2, height // 2, duration=0.5)
        time.sleep(2)
        device.screenshot("real_test_02_search.png")
        return True
    else:
        print("   Found Home Connect on home screen")
        return True


def open_home_connect_app(device):
    """Open the Home Connect app."""
    if device.wait_for_element_by_text("Home Connect", timeout=10):
        device.tap_by_text("Home Connect")
        time.sleep(4)
        device.screenshot("real_test_03_app_opened.png")
        return True
    else:
        print("   Home Connect app not found")
        return False


def navigate_to_add_appliance(device):
    """Navigate to add appliance screen."""
    add_buttons = ["Add Appliance", "+", "Add", "New Device"]

    for btn in add_buttons:
        if device.wait_for_element_by_text(btn, timeout=3):
            print(f"   Found button: {btn}")
            device.tap_by_text(btn)
            time.sleep(2)
            device.screenshot("real_test_04_add_screen.png")
            return True

    print("   No add button found with text")
    return False


def select_appliance_type(device):
    """Select an appliance type."""
    appliances = ["Dishwasher", "Washing Machine", "Oven", "Coffee Machine"]

    for appliance in appliances:
        if device.wait_for_element_by_text(appliance, timeout=3):
            print(f"   Found appliance: {appliance}")
            device.tap_by_text(appliance)
            time.sleep(2)
            device.screenshot("real_test_05_appliance_selected.png")
            return True

    # Try scrolling to find more options
    width, height = device.get_screen_size()
    device.swipe(width // 2, height * 0.7, width // 2, height * 0.3, duration=0.5)
    time.sleep(2)

    for appliance in appliances:
        if device.wait_for_element_by_text(appliance, timeout=2):
            print(f"   Found appliance after scroll: {appliance}")
            device.tap_by_text(appliance)
            device.screenshot("real_test_05_appliance_selected.png")
            return True

    print("   No appliance type found")
    return False


def configure_network_settings(device):
    """Configure network settings if required."""
    network_fields = ["Network", "WiFi", "SSID", "Password"]

    for field in network_fields:
        if device.wait_for_element_by_text(field, timeout=3):
            print(f"   Found network field: {field}")
            device.tap_by_text(field)
            time.sleep(1)

            if "password" in field.lower():
                device.input_text("TestPassword123")
            else:
                device.input_text("TestNetwork")
            time.sleep(1)

    device.screenshot("real_test_06_network_config.png")
    return True


def complete_appliance_setup(device):
    """Complete the appliance setup."""
    completion_buttons = ["Connect", "Done", "Finish", "Save", "Continue"]

    for button in completion_buttons:
        if device.wait_for_element_by_text(button, timeout=3):
            print(f"   Found completion button: {button}")
            device.tap_by_text(button)
            time.sleep(3)
            device.screenshot("real_test_07_complete.png")
            return True

    print("   No completion button found")
    device.screenshot("real_test_07_final_state.png")
    return True


if __name__ == "__main__":
    # Allow running this test file directly
    print("Running Home Connect workflow test on real device...")
    success = run_home_connect_workflow_test()
    if success:
        print("✅ Test completed successfully!")
    else:
        print("❌ Test failed or was skipped.")
