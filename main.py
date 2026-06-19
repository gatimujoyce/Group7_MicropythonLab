import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

#  WiFi Config 
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

#  MQTT Config 
MQTT_CLIENT_ID = "ics4111-group7-esp32"
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

#  Sensor 
sensor = dht.DHT22(Pin(4))

#  Connecting to WiFi 
print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")
print("IP Address:", sta_if.ifconfig()[0])

# Connecting to MQTT Broker
print("Connecting to MQTT broker...", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
client.connect()
print(" Connected!")


print("\n=== ICS 4111 IoT Lab - DHT22 Sensor ===")
print("Publishing to topic:", MQTT_TOPIC)
print("-" * 45)

reading_count = 0

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        reading_count += 1

        payload = ujson.dumps({
            "reading": reading_count,
            "temperature": temperature,
            "humidity": humidity
        })

        client.publish(MQTT_TOPIC, payload)
        print(f"[{reading_count:03d}] Published: {payload}")

    except OSError as e:
        print(f"Error: {e}")

    time.sleep(3)