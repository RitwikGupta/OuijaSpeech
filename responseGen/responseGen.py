#!/usr/bin/env python

import cleverbot
import sys
import string
import serial
import time
from functools import wraps
import errno
import os
import signal
import requests
from timeout import timeout

def mainFunction():
    qu = sys.argv[1]
    print "Query: " + qu
    user = "Yolo!"

    if(qu == "-1"):
        response = "&"

    elif(qu == "-2"):
        response = "+&"

    else:
        cb1 = cleverbot.Cleverbot()

        response = cb1.ask(qu)
        print "Response: " + response
        #Replace all punctuation with blanks
        for c in string.punctuation:
            response = response.replace(c, "")

        while (response.find("app") != -1 or response.find("clever") != -1 or response.find("bot") != -1 or response.find("com") != -1):
            response = cb1.ask(qu)

        respon = response.strip()

        #Make all spaces periods
        response = response.replace(" ", ".").strip()
        response = response.lower() + "&"

    username = sys.argv[2]

    if username == "None":
        pass

    elif response != "&":
        if response == "+&":
            respo = "Yo"
            que = "Yo"
        else:
            respo = respon
            que = qu
        user = username
        conversation = str(user) + "said: " + str(que) + " <br>" + "Bot responded: " + str(respo) + " <br><hr>"
        requestURL = "http://www.purduecs.com/write.php?username=" + str(user) + "&conversation=" + str(conversation)
        r = requests.get(requestURL)

    return response

response = mainFunction()

print response

ser = serial.Serial('/dev/ttyACM0', 57600)
ser.write(response)

#while True:
	#print ser.readline()
