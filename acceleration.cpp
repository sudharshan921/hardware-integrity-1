const int throttleInputPin = A0;  // Analog input pin for throttle signal
const int throttleOutputPin = 9;  // PWM output pin for throttle control

void setup() {
  Serial.begin(9600);  // Initialize serial communication
  pinMode(throttleOutputPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the command from the serial port
    char command = Serial.read();
    Serial.flush();  // Clear the serial buffer
    
    if (command == 'r') {
      // Read the throttle signal and send it to the computer
      int throttleValue = analogRead(throttleInputPin);
      Serial.println(throttleValue);
    } else if (command == 'w') {
      // Wait for the throttle value to arrive
      while (Serial.available() == 0) {}
      int throttleValue = Serial.parseInt();
      analogWrite(throttleOutputPin, map(throttleValue, 0, 1023, 0, 255));
    }
    delay(10);  // Small delay to ensure processing time
  }
}
