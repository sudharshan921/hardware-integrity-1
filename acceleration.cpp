const int throttleInputPin = A0;  
const int throttleOutputPin = 9;  

void setup() {
  Serial.begin(9600);  
  pinMode(throttleOutputPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    
    char command = Serial.read();
    Serial.flush();  
    
    if (command == 'r') {
      
      int throttleValue = analogRead(throttleInputPin);
      Serial.println(throttleValue);
    } else if (command == 'w') {

      while (Serial.available() == 0) {}
      int throttleValue = Serial.parseInt();
      analogWrite(throttleOutputPin, map(throttleValue, 0, 1023, 0, 255));
    }
    delay(10);  
  }
}
