#!/usr/bin/env python

import cleverbot
import sys
import string
import serial
import time

qu = sys.stdin.readlines()[0].strip()

if(qu == "-1"):
    response = "&"
else:
    cb1 = cleverbot.Cleverbot()

    response = cb1.ask(qu)

    #Replace all punctuation with blanks
    for c in string.punctuation:
        response = response.replace(c, "")

    while (response[0] == "*" or response.find("app") != -1 or response.find("clever") != -1 or response.find("bot") != -1 or response.find("com") != -1):
      response = cb1.ask(qu)

    #Make all spaces periods
    response = response.replace(" ", ".")
    response = response.lower() + "&"

ser = serial.Serial('/dev/tty.usbmodem1421', 57600)

time.sleep(3)

ser.write(response)

#while True:
	#print ser.readline()
