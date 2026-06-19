# group7_micropythonlab

ICS 4111: Embedded Systems & IoT — MicroPython IoT Lab (Group 7)

## Overview

This project implements an end-to-end IoT sensor pipeline using MicroPython. A DHT22 sensor connected to a TTGO LoRa32 board reads temperature and humidity, publishes the readings as JSON over MQTT, and a PC-side Python subscriber receives the messages and persists them to a local SQLite database.

**Data flow:** DHT22 → TTGO (MicroPython) → WiFi → MQTT Broker (`broker.emqx.io`) → PC Subscriber (`paho-mqtt`) → SQLite Database

## Hardware Used

| Component | Notes |
|---|---|
| TTGO LoRa32 board | ESP32-based microcontroller, used in place of a generic ESP32 DevKit |
| DHT22 (AM2302) | Temperature/humidity sensor |
| Breadboard | For prototyping the circuit |
| Jumper wires (male-to-male) | Connect TTGO pins to breadboard and DHT22 |
| 10 kΩ resistor | Pull-up on the DHT22 data line |
| USB data cable | Must be data-capable: charge-only cables will not be detected for flashing |

## Wiring

| DHT22 Pin | TTGO Pin |
|---|---|
| VCC | 5V |
| SDA (Data) | GPIO 4 |
| GND | GND |
| 10 kΩ resistor between 5V row and GPIO 4 row (pull-up) |

See `screenshots/breadboard_wiring.png` for the annotated physical wiring.

## Repository Structure

```
group7_micropythonlab/
├── README.md
├── main.py                  # MicroPython script (runs on the TTGO)
├── subscriber.py            # PC-side MQTT subscriber + SQLite writer
├── check_db.py              # Verifies stored readings in SQLite
├── diagram.json             # Wokwi simulation circuit (simulation phase)
└── screenshots/
    ├── breadboard_wiring.png
    ├── repl_output.png
    ├── mqtt_subscriber_terminal.png
    ├── formatted_sqlite_query_result.png 
    └── sqlite_query_result.png
```

## Software Requirements

- [Thonny IDE](https://thonny.org/) (or any MicroPython-compatible IDE)
- [esptool](https://pypi.org/project/esptool/) — flashes MicroPython firmware to the board
- [MicroPython firmware for ESP32](https://micropython.org/download/ESP32_GENERIC/) (v1.24+)
- Python 3.9+ (for the PC-side subscriber)
- `paho-mqtt`


## Setup & Usage

### 1. Flash MicroPython onto the TTGO

```bash
python -m esptool --port COMx erase-flash
python -m esptool --port COMx --baud 460800 write-flash -z 0x1000 <firmware>.bin
```

Replace `COMx` with your board's serial port and `<firmware>.bin` with the downloaded MicroPython image.

### 2. Configure WiFi credentials

Before uploading, edit `main.py` and set your network credentials:

```python
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

### 3. Upload and run `main.py`

Open `main.py` in Thonny with the board connected, then save it to the device and run it. The REPL should show the board connecting to WiFi, connecting to the MQTT broker, and publishing readings every 3 seconds.

### 4. Run the PC-side subscriber

```bash
python subscriber.py
```

This connects to the same MQTT broker and topic, receives incoming readings, and stores them in `sensor_data.db`.

### 5. Verify stored data

```bash
python check_db.py
```

This prints all stored rows from the SQLite database in a readable table format.

## MQTT Configuration

| Setting | Value |
|---|---|
| Broker | `broker.emqx.io` |
| Port | `1883` |
| Topic | `iot/lab/sensor` |
| Payload format | JSON: `{"reading": <int>, "temperature": <float>, "humidity": <float>}` |

## Database Schema

```sql
CREATE TABLE readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    humidity REAL,
    reading_number INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Evidence / Screenshots

| File | Description |
|---|---|
| `screenshots/breadboard_wiring.png` | Annotated DHT22–TTGO wiring on breadboard |
| `screenshots/repl_output.png` | TTGO REPL showing WiFi + MQTT connection and live published readings |
| `screenshots/mqtt_subscriber_terminal.png` | PC subscriber receiving and saving 10+ messages |
| `screenshots/formatted_sqlite_query_result.png` |Formatted SQLite `SELECT` query confirming stored readings with timestamps |
| `screenshots/sqlite_query_result.png` | SQLite `SELECT` query confirming stored readings with timestamps |

## Team

**Group 7**
- Gatimu Joyce Wanjiru – 169203
  

## Course

ICS 4111: Embedded Systems & IoT, Strathmore University, School of Computing & Engineering Sciences (Apr–Jul 2026)
