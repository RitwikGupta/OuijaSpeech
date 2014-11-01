#!/usr/bin/env python

import speech_recognition as sr
import time
r = sr.Recognizer()

start = end = time.time()
# while True:
with sr.Microphone() as source:
    r.energy_threshold = 100
    audio = r.listen(source, timeout = 1)

end = time.time()

# print "Took", (end-start), "seconds"

start = end = time.time()
    
try:
    print r.recognize(audio)

except LookupError:
    print "-1"
