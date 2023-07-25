#include <Servo.h>

Servo myservo;  // create servo object to control a servo

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);  // start serial communication at 9600bps
}

void loop() {
  if (Serial.available() > 0) {  // if data is available to read
    String data = Serial.readString();  // read it and store it in 'data'
    data.trim();
    if (data == "FIRE!") {  // if fire command is received
      myservo.write(25);  // tell servo to go to fire position
      delay(50); // wait for a bit
      myservo.write(0); // reset servo position
    }
  }
}

