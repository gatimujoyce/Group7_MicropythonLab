import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime

# MQTT Config
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/lab/sensor"

# SQLite Setup 
def init_db():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            reading_number INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def save_reading(conn, temperature, humidity, reading_number):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO readings (temperature, humidity, reading_number, timestamp)
        VALUES (?, ?, ?, ?)
    """, (temperature, humidity, reading_number, datetime.now()))
    conn.commit()
    print(f"  >>> Saved to DB: Temp={temperature}°C, Humidity={humidity}%, Reading={reading_number}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        print(f"Subscribing to topic: {MQTT_TOPIC}")
        client.subscribe(MQTT_TOPIC)
        print("Waiting for messages...\n" + "-" * 45)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        temperature = payload["temperature"]
        humidity = payload["humidity"]
        reading_number = payload["reading"]

        print(f"[{reading_number:03d}] Received: Temp={temperature}°C | Humidity={humidity}%")
        save_reading(userdata, temperature, humidity, reading_number)

    except Exception as e:
        print(f"Error processing message: {e}")


print("=== ICS 4111 IoT Lab - MQTT Subscriber ===")
conn = init_db()
print("Database initialized: sensor_data.db")

client = mqtt.Client(userdata=conn)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()