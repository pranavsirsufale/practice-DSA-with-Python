import machine
import dht
import time
import network
# import urequests
import ujson
import os
import ntptime
from umqtt.simple import MQTTClient

WIFI_SSID = "Csit"
WIFI_PASS = "csitdept"
API_URL = "https://3000-firebase-temprature-data-1775386871390.cluster-bqwaigqtxbeautecnatk4o6ynk.cloudworkstations.dev/data"
LOG_FILE = "offline_data.json"


MQTT_BROKER = "test.mosquitto.org"
MQTT_CLIENT_ID = "esp32_dht11"
MQTT_TOPIC = b"sensor/data"

led = machine.Pin(2, machine.Pin.OUT)

sensor = dht.DHT11(machine.Pin(4))
wlan = network.WLAN(network.STA_IF)
mqttConnected = False

mqttClient = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)

def connectMQTT():
    global mqttConnected
    try:
        if not mqttConnected:
            mqttClient.connect()
            mqttConnected = True
            print("MQTT Connected!")
    except Exception as e:
        print("MQTT connection failed:", e)
        mqttConnected = False

def connectWIFI():
    try:
        if wlan.isconnected():
            return True

        wlan.active(True)
        if wlan.status() != network.STAT_CONNECTING:
            print("Connecting to WiFi...")
            wlan.connect(WIFI_SSID, WIFI_PASS)

        for _ in range(5): 
            if wlan.isconnected():
                print("WiFi Connected!")
                try:
                    ntptime.settime() # Sync time
                except:
                    pass 
                return True
            time.sleep(1)
            
        return False
        
    except OSError as e:
        print("WiFi Driver Error (State Error). Resetting interface...")
        wlan.active(False) # Turn it off
        time.sleep(1)
        wlan.active(True)  # Turn it back on to 'clear' the state
        return False

def saveLocally(data):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(ujson.dumps(data) + "\n")
        print("Data saved locally.")
    except Exception as e:
        print("Storage error:", e)

def syncData():
    try:
        files = os.listdir()
        if LOG_FILE not in files:
            return 
        
        print("Syncing...")
        with open(LOG_FILE, "r") as f:
            for line in f:
                cleanLine = line.strip()
                if cleanLine:
                    payload = ujson.loads(cleanLine)
                    mqttClient.publish(MQTT_TOPIC, ujson.dumps(payload))
                    # res = urequests.post(API_URL, json=payload)
                    # res.close()
        
        os.remove(LOG_FILE)
        print("Sync complete.")
    except Exception as e:
        print("Sync failed:", e)

while True:
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        currentUnixTime = time.time() + 946684800
        payload = {"temp": t,"hum": h,"timestamp": currentUnixTime}

        if connectWIFI():
            connectMQTT()
            if mqttConnected:
                try:
                    led.value(1)
                    syncData()
                    mqttClient.publish(MQTT_TOPIC, ujson.dumps(payload))
                    print("Published via MQTT:", payload)
                    led.value(0)
                except Exception as e:
                    print("MQTT Error:", e)
                    mqttConnected = False
                    print("saving locally...")
                    saveLocally(payload)
        else:
            print("saving locally...")
            saveLocally(payload)
            
    except Exception as e:
        import sys
        print("Loop error:")
        sys.print_exception(e)
        
    time.sleep(10)





