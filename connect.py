import simplepyble
import struct

if __name__ == "__main__":
    adapters = simplepyble.Adapter.get_adapters()

    if len(adapters) == 0:
        print("No adapters found")
        exit()

    # Query the user to pick an adapter
    print("Please select an adapter:")
    for i, adapter in enumerate(adapters):
        print(f"{i}: {adapter.identifier()} [{adapter.address()}]")

    choice = int(input("Enter choice: "))
    adapter = adapters[choice]

    print(f"Selected adapter: {adapter.identifier()} [{adapter.address()}]")

    adapter.set_callback_on_scan_start(lambda: print("Scan started."))
    adapter.set_callback_on_scan_stop(lambda: print("Scan complete."))
    adapter.set_callback_on_scan_found(lambda peripheral: print(f"Found {peripheral.identifier()} [{peripheral.address()}]"))

    # Scan for 5 seconds
    adapter.scan_for(5000)
    peripherals = adapter.scan_get_results()

    if len(peripherals) == 0:
        print("No peripherals found")
        exit()

    # Query the user to pick a peripheral
    print("Please select a peripheral:")
    for i, peripheral in enumerate(peripherals):
        print(f"{i}: {peripheral.identifier()} [{peripheral.address()}]")

    choice = int(input("Enter choice: "))
    peripheral = peripherals[choice]

    print(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
    peripheral.connect()

    print("Successfully connected, listing services...")
    services = peripheral.services()
    for service in services:
        print(f"Service: {service.uuid()}")
        for characteristic in service.characteristics():
            print(f"    Characteristic: {characteristic.uuid()}")

            # Assuming the data characteristic UUID is 979b5a11-81e8-4531-89c9-90024f2984a2
            if characteristic.uuid() == "979b5a11-81e8-4531-89c9-90024f2984a2":
                print("Subscribing to notifications...")
                characteristic.start_notify()

                # Handle notifications from the data characteristic
                while True:
                    try:
                        notification = characteristic.wait_for_notification(timeout=10)
                        if notification:
                            light_data = notification.data
                            light_value = struct.unpack('<f', light_data)[0]
                            print(f"Received Light Sensor Data: {light_value}")
                    except simplepyble.exceptions.BLENotificationTimeout:
                        print("No notification received within the timeout.")
                        break

                characteristic.stop_notify()

    peripheral.disconnect()
