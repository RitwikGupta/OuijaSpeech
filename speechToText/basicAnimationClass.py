# basicAnimationClass.py
# version 0.5

from Tkinter import *
from basicAnimation import BasicAnimationRunner

class BasicAnimationClass(object):
    # Override these methods (or not)
    def onMousePressed(self, event): pass
    def onKeyPressed(self, event): pass
    def onTimerFired(self): pass
    def redrawAll(self): pass
    def initAnimation(self): pass

    # If you override this, be sure to still call it via super.__init__
    def __init__(self, width=300, height=300):
        self.width = width
        self.height = height

    # In general, you would probably not override this method (but you could)
    def run(self):
        def myBasicAnimation(app, canvas):
            self.app = app
            self.canvas = canvas
            self.initAnimation()
            while app.isRunning():
                (eventType, event) = app.getEvent()
                if (eventType == "mousePressed"): self.onMousePressed(event)
                elif (eventType == "keyPressed"): self.onKeyPressed(event)
                elif (eventType == "timerFired"): self.onTimerFired()
                self.redrawAll()
            print "Done!"
        BasicAnimationRunner(myBasicAnimation, width=self.width, height=self.height)
