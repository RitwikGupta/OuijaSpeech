// Harris Christiansen (HarrisChristiansen.com)
// 2014-10-31
// For YHack - Ouija Board

#include <Servo.h>

Servo servoX, servoY;

int motorX = 4;
int motorY = 8;

char runningQue[40];
char inChar=-1;
byte index = 0;

int coordinatesTable[40][3] = {
              85,162,'a', 78,162,'b', 71,162,'c', 65,162,'d', 58,162,'e', 52,162,'f', 46,162,'g', 40,162,'h',
  89,168,'i', 85,168,'j', 78,168,'k', 71,168,'l', 65,168,'m', 58,168,'n', 52,168,'o', 46,168,'p', 40,168,'q', 35,168,'r',
              85,174,'s', 78,174,'t', 71,174,'u', 65,174,'v', 58,174,'w', 52,174,'x', 46,174,'y', 40,174,'z',
  89,180,'0', 85,180,'1', 78,180,'2', 71,180,'3', 65,180,'4', 58,180,'5', 52,180,'6', 46,180,'7', 40,180,'8', 35,180,'9',
  90,155,'+', //Yo
  34,155,'&', //End of Sent
  0,0,'!', //Do Corners
  0,0,'.' //SPACE
};

int noteFreqArr[24] = { // For Music
 // First Octave
 523.3, // C  0
 554.4, // C# 1
 587.3, // D  2
 622.3, // Ef 3
 659.3, // E  4
 698.5, // F  5
 740.0, // F# 6
 784.0, // G  7
 830.6, // G# 8
 880.0, // A  9
 932.3, // Bf 10
 987.8, // B  11
 // Second Octave 
 1047, // C 12
 1109,  // C# 13
 1175,  // D 14
 1245,  // Ef 15
 1319,  // E 16
 1397,  // F 17
 1480,  // F# 18
 1568,  // G 19
 1661,  // G# 20
 1760,  // A  21
 1865,  // Bf  22
 1976   // B   23
};

void setup() {
  Serial.begin(57600);
  runningQue[0] = '\0';
  
  // Servo Setup
  servoX.attach(motorX);
  servoY.attach(motorY);
  
  // Music Setup
  pinMode(5, OUTPUT);
}

void loop() {
  delay(20);
  readSerial();
  while(runningQue[0] != '\0') {
    printArray();
    goTo();
    delay(600);
  }
}

void readSerial() {
  while(Serial.available() > 0) {
    if(index < 39) {
      inChar = Serial.read();
      runningQue[index] = inChar;
      index++;
      runningQue[index] = '\0';
    }
  }
  index = 0;
}

void printArray() {
  Serial.println(runningQue);
}

int lastPos = 0;
void goTo() {
  int nextPos = getNextPos();
  if(nextPos>39 || nextPos<0) { return; }
  if(nextPos == 39) { return; }
  if(nextPos == 38) { // Show Corners
    servoX.write(85);
    servoY.write(162);
    delay(1000);
    servoX.write(40);
    servoY.write(162);
    delay(1000);
    servoX.write(35);
    servoY.write(180);
    delay(1000);
    servoX.write(89);
    servoY.write(180);
    delay(1000);
    return;
  }
  
  Serial.print("Moving To: ");
  Serial.print(coordinatesTable[nextPos][0]);
  Serial.print(" ");
  Serial.println(coordinatesTable[nextPos][1]);
  
  // Set Angles
  if(nextPos == lastPos) {
    servoX.write(coordinatesTable[nextPos][0]);
    servoY.write(coordinatesTable[nextPos][1]-10);
    delay(100);
    servoX.write(coordinatesTable[nextPos][0]);
    servoY.write(coordinatesTable[nextPos][1]);
  } else {
    servoX.write(coordinatesTable[nextPos][0]);
    servoY.write(coordinatesTable[nextPos][1]);
    if(nextPos == 36) {
      playSongOne();
    }
    delay(100);
    servoX.write(coordinatesTable[nextPos][0]);
    servoY.write(coordinatesTable[nextPos][1]);
  }
  
  lastPos = nextPos;
}

char getNextPos() {
  char returnChar = runningQue[0];
  for(int i = 0; i < 39; i++) {
    runningQue[i] = runningQue[i+1];
  }
  
  for(int i = 0; i <= 39; i++) {
    if(returnChar == (char)coordinatesTable[i][2]) {
      return i;
    }
  }
  
  return -1; // Char Not Found
}

//// Music ////

void playNote(int noteInt, long length, long breath = 20) {
 length = length - breath;
 buzz(5, noteFreqArr[noteInt], length);
 if(breath > 0) { //take a short pause or 'breath' if specified
   delay(breath);
 }
}

void buzz(int targetPin, long frequency, long length) {
 long delayValue = 1000000/frequency/2; // calculate the delay value between transitions
 //// 1 second's worth of microseconds, divided by the frequency, then split in half since
 //// there are two phases to each cycle
 long numCycles = frequency * length/ 1000; // calculate the number of cycles for proper timing
 //// multiply frequency, which is really cycles per second, by the number of seconds to 
 //// get the total number of cycles to produce
 for (long i=0; i < numCycles; i++){ // for the calculated length of time...
   digitalWrite(targetPin,HIGH); // write the buzzer pin high to push out the diaphram
   delayMicroseconds(delayValue); // wait for the calculated delay value
   digitalWrite(targetPin,LOW); // write the buzzer pin low to pull back the diaphram
   delayMicroseconds(delayValue); // wait againf or the calculated delay value
 }
}

void playSongOne() {
   playNote(12, 300);
   playNote(19, 300);
   playNote(23, 300);
   playNote(18, 300);
  
   playNote(12, 300);
   playNote(19, 300);
   playNote(23, 300);
   playNote(18, 300);
  
   playNote(12, 300);
   playNote(19, 300);
   playNote(23, 300);
   playNote(18, 300);
}

