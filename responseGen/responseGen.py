import cleverbot
import sys

qu = sys.stdin.readlines()

cb1 = cleverbot.Cleverbot()
print cb1.ask(qu)
