import machine
import dht
import time
import network
import urequests
import ujson
import os
import ntptime

WIFI_SSID = "Csit"
WIFI_PASS = "csitdept"
API_URL = "https://3000-firebase-temprature-data-1775386871390.cluster-bqwaigqtxbeautecnatk4o6ynk.cloudworkstations.dev/data"
LOG_FILE = "offline_data.json"

sensor = dht.DHT11(machine.Pin(4))
wlan = network.WLAN(network.STA_IF)

def connectWIFI():
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        for _ in range(10):
            if wlan.isconnected():
                print("WiFi Connected! Waiting for IP...")
                try:
                    ipAddress = wlan.ifconfig()[0]
                    print("My IP address is:", ipAddress)
                    ntptime.host = "time.google.com" # Often more reliable than pool.ntp.org
                    ntptime.settime()
                    print("Clock synced to:", time.localtime())
                except Exception as e:
                    print("NTP sync failed:", e)
                break
            time.sleep(1)
    print("Wifi connection status is :", wlan.isconnected())
    return wlan.isconnected()

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
                    res = urequests.post(API_URL, json=payload)
                    res.close()
        
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

        payload = {
            "temp": t,
            "hum": h,
            "timestamp": currentUnixTime
        }

        if connectWIFI():
            syncData()
            print("Sending current data...")
            res = urequests.post(API_URL, json=payload, timeout=10)
            res.close()
            print("Success:", payload)
        else:
            print("saving locally...")
            saveLocally(payload)
            
    except Exception as e:
        import sys
        print("Loop error:")
        sys.print_exception(e)
        
    time.sleep(10)

