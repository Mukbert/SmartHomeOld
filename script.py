import Adafruit_DHT
import sys, time, os 

DHT_PIN = 23
DHT_SENSOR = Adafruit_DHT.DHT11

def get_humidity():
	humidity, _ = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, retries=20)
	return humidity