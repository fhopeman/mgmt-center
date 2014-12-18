import smbus
import time

bus = smbus.SMBus(1)

def slaveCall(address, cmd):
    bus.write_byte(address, cmd)

def slaveRead(address, digits):
    time.sleep(0.01)
    res = ""
    for i in range(0, digits):
        c = chr(bus.read_byte(address));
        # better to handle in arduinoSlave.ino (don't send such values)
        if (c != '\x00'):
          res += c
          time.sleep(0.01)

    return res
