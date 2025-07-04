#include <Servo.h>

// Define servos for each finger
Servo thumb, index, middle, ring, pinky;

// Define pin numbers for servos
const int thumbPin = 3;
const int indexPin = 5;
const int middlePin = 6;
const int ringPin = 9;
const int pinkyPin = 10;

void setup() {
    Serial.begin(9600); // Start Serial communication

    // Attach servo motors to their respective pins
    thumb.attach(thumbPin);
    index.attach(indexPin);
    middle.attach(middlePin);
    ring.attach(ringPin);
    pinky.attach(pinkyPin);
}

void loop() {
    if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');  // Read data until newline

    if (data.length() == 5) {  // Ensure valid data length
        Serial.println("Received: " + data);  // Print received data
        
        // Invert thumb logic only
        controlFinger(thumb, data[0] == '1' ? '0' : '1');
        controlFinger(index, data[1]);
        controlFinger(middle, data[2]);
        controlFinger(ring, data[3]);
        controlFinger(pinky, data[4]);
    }
}

}

// Function to control finger servos
void controlFinger(Servo &finger, char state) {
    if (state == '1') {
        finger.write(180); // Open position
    } else {
        finger.write(0); // Closed position
    }
}


