#!/usr/bin/python
import RPi.GPIO as GPIO

import signal
import sys
import time
import usb

## Function definitions

# Init all pins
def initPins():
  GPIO.setup(7, GPIO.OUT)

# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
    GPIO.cleanup()
    exit(0)


## Main section

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)

# Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Init pins
initPins()

freq=440.0

# What USB busses are availible?
busses = usb.busses()

ai = None

# We only need the ASUS Ai Remote
while not ai:
    for bus in busses:
        for dev in bus.devices:
            if dev.idVendor == 0x0b05 and dev.idProduct == 0x172e:
                print ('ASUS Ai Remote found.')
                ai = dev

# We're still there so we open the device
handler = ai.open()

# If the remote isn't found - exit
if not ai:
    print ('No Device found!')
    exit()

# We know that there is only one configuration
conf = ai.configurations[0]
# Only one interface
iface = conf.interfaces[0][0]
# Only one endpoint
endp = iface.endpoints[0]

# We don't want the kernel to handle this device
try:
    handler.detachKernelDriver(iface)
except usb.USBError, e:
    print (e.args[0])
    if e.args != ('could not detach kernel driver from interface 0: No data available',):
        raise e

print(str(freq) + " Hz")

while True:
  # Play sound
  GPIO.output(7, GPIO.HIGH)
  time.sleep((1/freq)/2)
  GPIO.output(7, GPIO.LOW)
  time.sleep((1/freq)/2)

  # Read input from remote
  data = (2,0,0,0,0,0,0,0)
  try:
    data = handler.interruptRead(endp.address, endp.maxPacketSize,1)
  except (usb.USBError, e):
    if e.args != ('No error',) and e.args != ('could not detach kernel driver from interface 0: No data available',): # http://bugs.debian.org/476796
      raise e


# Below is the codes associated to remote buttons.
#
# 1
# 6  -  3 - 4
# 12 - 13 - 5
#
#      7
#  8 - 9 - 10
#     11
#
# We're just looking for "+" and "-" buttons, so "7" and "11" codes

  if data[1] != 0:
    if data[1] == 7:
      # "+" button was pressed
      freq = freq + 1000
      print(str(freq) + " Hz")
    if data[1] == 11:
      # "-" button was pressed
      freq = freq - 1000
      print(str(freq) + " Hz")
    if data[1] == 1:
      # "Power" butto was pressed
      GPIO.cleanup()
      exit(0)

