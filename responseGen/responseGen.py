#!/usr/bin/env python

import cleverbot
import sys

qu = sys.stdin.readlines()

cb1 = cleverbot.Cleverbot()

response = cb1.ask(qu)
while response[0] == "*":
  response = cb1.ask(qu)

print response
