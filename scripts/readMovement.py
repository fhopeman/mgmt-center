#!/usr/bin/python

import time
import sys
import RPi.GPIO as io

def read_movement(pin):
    while True:
        if io.input(pin):
            print("ALARM!")
        time.sleep(0.5)

# Parse command line parameters
if len(sys.argv) == 2:
    pin = int(sys.argv[1])
    io.setmode(io.BCM)
    io.setup(pin, io.IN)
    print read_movement(pin)
else:
    print 'usage: sudo ./readMovement.py gpio-pin#'
    sys.exit(1)
