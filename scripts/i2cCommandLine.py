#!/usr/bin/python

import smbus
import time
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

def writeNumber(address, cmd):
    bus.write_byte(address, cmd)
    return -1

def readRes(address, digits):
    res = ""
    for i in range(0, digits):
        res += chr(bus.read_byte(address))
        time.sleep(0.01)
    
    return res

while True:
    # select nano
    nano = input("nano: ")
    if (nano == 0):
        address = 0x04
    if (nano == 1):
        address = 0x24

    # select cmd
    cmd = input("cmd: ")
    writeNumber(address, cmd)

    if (cmd >= 10 and cmd <= 19):
        time.sleep(0.01)
        print "ALARM_RES: ", readRes(address, 1)

    if (cmd >= 20 and cmd <= 29):
        time.sleep(0.01)
        print "LED_RES: ", readRes(address, 1)

    if (cmd >= 30 and cmd <= 39):
        time.sleep(0.01)
        print "ENV_RES: ", readRes(address, 10)
