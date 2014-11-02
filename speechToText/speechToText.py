import speech_recognition as sr
from Tkinter import *
from basicAnimationClass import BasicAnimationClass
import time
import math
import subprocess
import requests

class speechToText(BasicAnimationClass):
    def __init__(self, width=800, height=600):
        self.width = canvasWidth = width
        self.height = canvasHeight = height
        self.cx = self.width/2
        self.cy = self.height/2
        self.radius = 40
        super(speechToText, self).__init__(canvasWidth, canvasHeight)

    def redrawAll(self):
        outlineColor = "white"
        cx, cy, r = self.cx, self.cy, self.radius
        userString = ""
        self.canvas.delete(ALL)
        if self.username != "None":
            username = (self.username).replace("0710106541", "")
        else:
            username = "None"
        self.canvas.create_text(cx, cy/3, text="OuijaBot", fill="white", font="Arial 30 bold")
        if username != "None":
            userString = "Conversation with " + username
            self.canvas.create_text(cx, self.height - r/2, text=userString, font="Arial 20 bold", fill=outlineColor)
        if self.isRecording:
            outlineColor = "red"
            self.canvas.create_oval(cx-(r/3), cy-(r/3), cx+(r/3), cy+(r/3), fill=outlineColor)
            self.canvas.create_text(cx, cy/2, text="Recording...", fill=outlineColor, font="Arial 20 bold")
            self.canvas.create_text(cx, cy/2 + 23, text="(stops automatically)", fill=outlineColor, font="Arial 15")
        elif self.checkingForYo:
            outlineColor = "purple"
            self.canvas.create_text(cx, cy, fill=outlineColor, text="Yo", font="Arial 20 bold")
            self.canvas.create_text(cx, cy/2, text="Checking for Yo's...", fill=outlineColor, font="Arial 20 bold")
        elif self.receivedAYo == False:
            outlineColor = "white"
            self.canvas.create_text(cx, cy/2, text="Click the button the start recording", fill=outlineColor, font="Arial 20 bold")
            self.canvas.create_oval(cx-(r/3), cy-(r/3), cx+(r/3), cy+(r/3), fill=outlineColor)

        if self.receivedAYo == False:
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, width=4, fill=None, outline=outlineColor)
        else:
            outlineColor = "white"
            self.canvas.create_rectangle(cx-r-10, cy-r-10, cx+r+10, cy+r+10, width=4, fill="white")
            self.canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, width=4, fill="purple", outline="white")
            self.canvas.create_text(cx, cy, fill=outlineColor, text="Yo", font="Arial 30 bold")

    def onTimerFired(self):
        if self.username == "None":
            self.checkingForYo = True
            self.redrawAll()
            r = requests.get('http://www.purduecs.com')
            self.checkingForYo = False
            if r.text != "No":
                self.receivedAYo = True
                if self.receivedAYo == True:
                    self.username = r.text
            time.sleep(1)
            self.redrawAll()
            try:
                subprocess.call(["../responseGen/responseGen.py", "-2", self.username])
            except:
                pass
            time.sleep(3)
            self.receivedAYo = False
            self.redrawAll()

    def onMousePressed(self, event):
        distance = math.sqrt((event.x - self.cx)**2 + (event.y - self.cy)**2)
        if distance <= self.radius:
            self.isRecording = True
            self.redrawAll()
            self.getText()
        else:
            self.isRecording = False
            self.redrawAll()

    def onKeyPressed(self, event):
        keysym = event.keysym
        if keysym == "r" or keysym == "y" or keysym == "o":
            if self.username != "None":
                readURL = "http://www.purduecs.com/read.php?username=" + str(self.username)
                user = str(self.username)
                requests.post("http://api.justyo.co/yo/", data={'api_token': "ec7efb15-f6e3-4548-91f3-81daf06446b2", 'username': user, 'link': readURL})
                self.username = "None"

    def getText(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.energy_threshold = 100
            audio, fuckedUp = r.listen(source, timeout = 1)
            self.isRecording = False
            self.redrawAll()

            try:
                subprocess.call(["../responseGen/responseGen.py", str(r.recognize(audio, fuckedUp)), self.username])
            except LookupError:
                subprocess.call(["../responseGen/responseGen.py", "-1", self.username])

    def initAnimation(self):
        self.isRecording = False
        self.app.setTimerDelay(15000) # every fifteen seconds
        self.checkingForYo = False
        self.receivedAYo = False
        self.username = "None"

stt = speechToText(800, 600)

stt.run()
