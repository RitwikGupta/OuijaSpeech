import speech_recognition as sr
from Tkinter import *
from basicAnimationClass import BasicAnimationClass
import time
import math

class speechToText(BasicAnimationClass):
    def __init__(self, width=800, height=600):
        self.width = canvasWidth = width
        self.height = canvasHeight = height
        self.cx = self.width/2
        self.cy = self.height/2
        self.radius = 40
        super(speechToText, self).__init__(canvasWidth, canvasHeight)
        
    def redrawAll(self):
        cx, cy, r = self.cx, self.cy, self.radius
        self.canvas.delete(ALL)
        if self.isRecording:
            outlineColor = "red"
            self.canvas.create_oval(cx-(r/3), cy-(r/3), cx+(r/3), cy+(r/3), fill=outlineColor)
            self.canvas.create_text(cx, cy/2, text="Recording...", fill=outlineColor, font="Arial 20 bold")
        else:
            outlineColor = "white"
            self.canvas.create_polygon(cx-(r/3), cy-(r/3), cx-(r/3), cy+(r/3), cx+(r/3), cy, fill=outlineColor)

        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, width=4, fill=None, outline=outlineColor)

    def onMousePressed(self, event):
        distance = math.sqrt((event.x - self.cx)**2 + (event.y - self.cy)**2)
        if distance <= self.radius:
            self.isRecording = True
            self.redrawAll()
            self.getText()
        else:
            self.isRecording = False
            self.redrawAll()

    def getText(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.energy_threshold = 100
            audio, fuckedUp = r.listen(source, timeout = 1)
            self.isRecording = False
            self.redrawAll()

            try:
                print r.recognize(audio, fuckedUp)

            except LookupError:
                print "-1"

    def initAnimation(self):
        self.isRecording = False

stt = speechToText(800, 600)

stt.run()

"""r = sr.Recognizer()

with sr.Microphone() as source:
    r.energy_threshold = 100
    audio = r.listen(source, timeout = 1)

    try:
        print r.recognize(audio)

    except LookupError:
        print "-1"""""
