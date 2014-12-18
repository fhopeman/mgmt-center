#!/usr/bin/python3

# Imports
import RPi.GPIO as gpio
import time

# Board setup
gpio.setmode(gpio.BCM)
# gpio.setup(2, gpio.IN)
gpio.setup(17, gpio.OUT)

# LED en/disable loop

print("enable GPIO17")
gpio.output(17, gpio.HIGH)

time.sleep(10)

print("disable GPIO17")
gpio.output(17, gpio.LOW)

time.sleep(10)

print("enable GPIO17")
gpio.output(17, gpio.HIGH)

time.sleep(10)

gpio.cleanup()
