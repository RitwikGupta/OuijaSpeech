#!/usr/bin/env python

import cleverbot
import sys
import string
import serial
import time

qu = sys.stdin.readlines()[0].strip()

if(qu == "-1"):
    print "What?"
else:
    cb1 = cleverbot.Cleverbot()

    response = cb1.ask(qu)

    #Replace all punctuation with blanks
    for c in string.punctuation:
        response = response.replace(c, "")

    #Make all spaces periods
    response = response.replace(" ", ".")

    while response[0] == "*":
      response = cb1.ask(qu)
    response = response.lower()  
    print response


ser = serial.Serial('/dev/tty.usbmodem1421', 57600)

time.sleep(3)

ser.write(response)

#while True:
	#print ser.readline()