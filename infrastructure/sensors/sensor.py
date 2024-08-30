import random
import time
import threading
import json
import paho.mqtt.client as mqtt

class Sensor:
    def __init__(self, sensor_id, sensor_type, mqtt_broker, mqtt_port):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.client = mqtt.Client()
        self.client.connect(self.mqtt_broker, self.mqtt_port)
        self.data = {}

    def read_data(self):
        # Simulate reading data from the sensor
        data = random.uniform(0, 100)
        self.data[self.sensor_type] = data
        return data

    def send_data(self):
        # Send data to the MQTT broker
        self.client.publish(f"sensors/{self.sensor_id}/{self.sensor_type}", json.dumps(self.data))
        print(f"Sending data from sensor {self.sensor_id} of type {self.sensor_type}: {self.data}")

    def start(self):
        # Start a thread to read and send data every 10 seconds
        def read_and_send_data():
            while True:
                self.read_data()
                self.send_data()
                time.sleep(10)
        threading.Thread(target=read_and_send_data).start()

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, mqtt_broker, mqtt_port):
        super().__init__(sensor_id, "temperature", mqtt_broker, mqtt_port)

class HumiditySensor(Sensor):
    def __init__(self, sensor_id, mqtt_broker, mqtt_port):
        super().__init__(sensor_id, "humidity", mqtt_broker, mqtt_port)

class PressureSensor(Sensor):
    def __init__(self, sensor_id, mqtt_broker, mqtt_port):
        super().__init__(sensor_id, "pressure", mqtt_broker, mqtt_port)

# Example usage:
if __name__ == "__main__":
    sensor1 = TemperatureSensor("sensor1", "localhost", 1883)
    sensor2 = HumiditySensor("sensor2", "localhost", 1883)
    sensor3 = PressureSensor("sensor3", "localhost", 1883)

    sensor1.start()
    sensor2.start()
    sensor3.start()

    while True:
        time.sleep(1)
