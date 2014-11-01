# basicAnimation.py (for CMU 15-112)
# version 0.5

# @TODO:
# immediate rather than deferred errors, say: create_line(range(100))

# Change log:
# 0.5: added optional keyword arguments passed through to appFn
# 0.5: fixed crash ("fn not defined") on reporting exception in canvas getattr
# 0.5: eliminated error on exit (just quit on WM_DESTROY_WINDOW, then destroy in canvas.after)
# 0.5: new, improved timerFired design (with separate timerFired thread)
# 0.4: added canvas.data Struct to wrapped canvas and basicAnimationDemo2.py
# 0.4: no hang when canvas methods called without getEvent
# 0.4: copy parameters on wrapped canvas calls to avoid destructive changes afterwards 
# 0.3: better error message on canvas.fn error

################################################
#
# See basicAnimationDemo.py for user documentation
#
# The code in this file is not intended for 112 students to
# even look at, let alone understand!
#
# For those who care, this code coerces Tkinter to let
# us use it from an external thread.  Then, we pretend
# this didn't happen, so that a programmer can use
# Tkinter graphics along with mouse, keyboard, and
# timer-based interactivity in what feels like a traditional,
# single-threaded, non-event-based, non-object-based way.
#
# We do this to get some simple interactive graphics into
# the early part of the course.  We absolutely double back
# later and do interactive graphics the "right" way,
# event-based and object-oriented.  And then, for the highly
# motivated, we may even explore all the yuck that went
# into this file to make their "simple" projects work at all.  :-)
#
# Bottom line: really nobody should ever use this code for
# anything beyond some really simple examples early on in a
# first programming course.
################################################

from Tkinter import *
from Queue import Queue
from threading import Thread
import sys, os, signal, copy, time

class Struct(object): pass

class BasicAnimationRunner(object):
    class WrappedCanvas(object):
        def __init__(self, app, drawingQueue):
            self.app = app
            self.data = Struct()
            self.drawingQueue = drawingQueue
            self.attrMap = { }
        def oops(self, msg):
            print "***********************"
            print msg
            os._exit(1)
        def __getattr__(self, name):
            fn = self.attrMap.get(name)
            if (fn == None):
                if ((name != "setTimerDelay") and
                    (self.app._getEventCalled == False)):
                    self.oops("(%s) You must call app.getEvent() after app.isRunning() and before using canvas!" % name)
                fn = lambda *args, **kwargs: self.drawingQueue.put((name,
                                                     copy.deepcopy(args),
                                                     copy.deepcopy(kwargs)))
                self.attrMap[name] = fn
            return fn

    def quit(self):
            self._isRunning = False
            self.eventQueue.put(("appClosed", None))
            try:
                if (self.runningInIDLE):
                    # in IDLE, must be sure to destroy here and now
                    self.root.destroy()
                else:
                    # not IDLE, then we'll destroy in the canvas.after handler
                    self.root.quit()
            except:
                pass
            #sys.exit(0)
            self.thread.join()

    def __init__(self, appFn, width=300, height=300, **kwargs):
        self.runningInIDLE =  ("idlelib" in sys.modules)    
        self.width = width
        self.height = height
        self.drawingQueue = Queue()
        self.eventQueue = Queue()
        self.eventQueue.put(("appLaunched", None))
        self._isRunning = True
        self._getEventCalled = False
        self.root = Tk()
        self.timerDelay = None # no timer by default
        self.timerThread = None
        self.timerFiredInQueue = False
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.quit())
        def onButtonPressed(event):
            if (not self._isRunning): return
            self.eventQueue.put(("mousePressed", event))
        self.root.bind("<Button-1>", onButtonPressed)
        def onKeyPressed(event):
            if (not self._isRunning): return
            self.eventQueue.put(("keyPressed", event))
        self.root.bind("<Key>", onKeyPressed)
        self.wrappedCanvas = self.WrappedCanvas(self, self.drawingQueue)
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.configure(background="black")
        self.canvas.pack()
        self.canvas.after(100, lambda: self.drawingQueueTimerFired())
        # get the app runner going in a new thread
        self.thread = Thread(target=lambda : appFn(self, self.wrappedCanvas, **kwargs))
        self.thread.daemon = True
        self.thread.start()
        # and then run the mainloop in this thread
        self.root.mainloop()

    def drawingQueueTimerFired(self):
        # clear drawing queue
        if (not self._isRunning):
            try:
                self.root.destroy()
            except:
                pass
            return
        while (not self.drawingQueue.empty()):
            (fnName, args, kwargs) = self.drawingQueue.get()
            if (not self._isRunning): break
            try:
                fn = getattr(self.canvas, fnName)
                fn(*args, **kwargs)
            except Exception as e:
                print "Error in canvas.%s: %s" % (fnName, str(e))
                #raise e
        self.canvas.update()
        self.canvas.after(100, lambda: self.drawingQueueTimerFired())

    def setTimerDelay(self, timerDelay):
        self.timerDelay = timerDelay
        if (self.timerThread == None):
            def timerThreadFn():
                while True:
                    if (not self._isRunning): return
                    if (self.timerFiredInQueue == False):
                        self.eventQueue.put(("timerFired", None))
                        self.timerFiredInQueue = True
                    delay = self.timerDelay/1000.0 if self.timerDelay else 1
                    time.sleep(delay)
            self.timerThread = Thread(target=timerThreadFn)
            self.timerThread.daemon = True
            self.timerThread.start()

    def isRunning(self):
        self._getEventCalled = False # need to call this again after each isRunning call
        return self._isRunning

    def getEvent(self, timeout=None):
        self._getEventCalled = True
        if (not self._isRunning): return ("appClosed", None)
        #self.clearDrawingQueue()
        if (timeout == None): timeout = self.timerDelay
        try:
            if ((timeout == None) or (timeout < 0)):
                result = self.eventQueue.get()
            else:
                result = self.eventQueue.get(True, timeout/1000.0)
        except:
            result = ("noEvent", None)
        if (result[0] == "timerFired"):
            self.timerFiredInQueue = False
        return result

# BasicAnimationRunner(myBasicAnimation, width=300, height=300)
