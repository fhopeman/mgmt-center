#!/usr/bin/python

import sys
import Adafruit_DHT

# Parse command line parameters.
if len(sys.argv) == 2:
	sensor = Adafruit_DHT.DHT22
	pin = sys.argv[1]
else:
	print 'usage: sudo ./Adafruit_DHT.py GPIOpin#'
	sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# If this happens try again!
if humidity is not None and temperature is not None:
	print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
else:
	print 'Failed to get reading. Try again!'
