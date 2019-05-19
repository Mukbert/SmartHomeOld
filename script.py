import Adafruit_DHT
import sys, time, os 

DHT_PIN = 23
DHT_SENSOR = Adafruit_DHT.DHT11

def get_humidity():
	humidity = None
	while humidity is None:
		humidity, _ = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
		if humidity is None:
			time.sleep(1.5)
	return humidity