import json
import paho.mqtt.client as mqtt
from iot_infrastructure.devices.device import Device

class Controller:
    def __init__(self, mqtt_broker, mqtt_port):
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.connect(self.mqtt_broker, self.mqtt_port)
        self.devices = {}

    def add_device(self, device):
        self.devices[device.device_id] = device

    def start_listening(self):
        # Subscribe to all device topics
        self.client.subscribe("devices/+")
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def on_message(self, client, userdata, message):
        # Handle incoming message from a device
        device_id = message.topic.split("/")[1]
        data = json.loads(message.payload)
        print(f"Received data from device {device_id}: {data}")
        # Process the data here, e.g., store it in a database or trigger an action

    def send_command(self, device_id, command):
        # Send a command to a device
        self.client.publish(f"devices/{device_id}/commands", json.dumps({"command": command}))
        print(f"Sending command to device {device_id}: {command}")

# Example usage:
if __name__ == "__main__":
    controller = Controller("localhost", 1883)

    device1 = SmartHomeDevice("device1", "localhost", 1883)
    device2 = IndustrialDevice("device2", "localhost", 1883)

    controller.add_device(device1)
    controller.add_device(device2)

    controller.start_listening()
