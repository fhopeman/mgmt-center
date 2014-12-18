#!/usr/bin/python

import sys, re

def read_sensor(device_id):
  value = None
  try:
    f = open("/sys/bus/w1/devices/" + device_id + "/w1_slave", "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(float(m.group(2)) / 1000.0)
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value

# Parse command line parameters.
# Known devices: 28-0004431e82ff
if len(sys.argv) == 2:
    device_id = sys.argv[1]
    print read_sensor(device_id)
else:
    print 'usage: sudo ./readTempDS18B20.py 1-wire-device-id'
    sys.exit(1)
