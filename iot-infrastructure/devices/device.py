import random
import time
import threading
import json
import paho.mqtt.client as mqtt

class Device:
    def __init__(self, device_id, device_type, mqtt_broker, mqtt_port):
        self.device_id = device_id
        self.device_type = device_type
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.connect(self.mqtt_broker, self.mqtt_port)
        self.sensors = {}
        self.data = {}

    def add_sensor(self, sensor):
        self.sensors[sensor.sensor_type] = sensor

    def read_data(self):
        # Read data from all sensors
        for sensor_type, sensor in self.sensors.items():
            self.data[sensor_type] = sensor.read_data()
        return self.data

    def send_data(self):
        # Send data to the MQTT broker
        self.client.publish(f"devices/{self.device_id}", json.dumps(self.data))
        print(f"Sending data from device {self.device_id} of type {self.device_type}: {self.data}")

    def start(self):
        # Start a thread to read and send data every 10 seconds
        def read_and_send_data():
            while True:
                self.read_data()
                self.send_data()
                time.sleep(10)
        threading.Thread(target=read_and_send_data).start()

class SmartHomeDevice(Device):
    def __init__(self, device_id, mqtt_broker, mqtt_port):
        super().__init__(device_id, "smart_home", mqtt_broker, mqtt_port)

class IndustrialDevice(Device):
    def __init__(self, device_id, mqtt_broker, mqtt_port):
        super().__init__(device_id, "industrial", mqtt_broker, mqtt_port)

# Example usage:
if __name__ == "__main__":
    device1 = SmartHomeDevice("device1", "localhost", 1883)
    device2 = IndustrialDevice("device2", "localhost", 1883)

    sensor1 = TemperatureSensor("sensor1", "localhost", 1883)
    sensor2 = HumiditySensor("sensor2", "localhost", 1883)
    sensor3 = PressureSensor("sensor3", "localhost", 1883)

    device1.add_sensor(sensor1)
    device1.add_sensor(sensor2)
    device2.add_sensor(sensor3)

    device1.start()
    device2.start()

    while True:
        time.sleep(1)
