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
from timeout import timeout

"""class TimeoutError(Exception):
    pass

def timeout(seconds=7, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator"""

def mainFunction():
    qu = sys.argv[1]

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

    return response

response = mainFunction()

print response

# ser = serial.Serial('/dev/tty.usbmodem1421', 57600)
#
# time.sleep(3)
#
# ser.write(response)

#while True:
	#print ser.readline()
