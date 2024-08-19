int soundSensorPin = A0;  // Define the sound sensor pin (analog pin A0)
int soundValue = 0;       // Variable to store the current sound value
int prevSoundValue = 0;   // Variable to store the previous sound value
int threshold = 7;        // Threshold to detect sound spikes
int debounceDelay = 100;  // Debounce delay to avoid false spikes
unsigned long lastSpikeTime = 0;  // Track the last significant sound spike

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud rate
}

void loop() {
  soundValue = analogRead(soundSensorPin);  // Read the analog value from the sound sensor

  // Apply a high-pass filter to cancel out low-frequency noise
  int filteredValue = soundValue - prevSoundValue;
  prevSoundValue = soundValue;

  // Check if the filtered value exceeds the threshold and debounce time has passed
  if (abs(filteredValue) > threshold && (millis() - lastSpikeTime) > debounceDelay) {
    Serial.println(filteredValue);  // Send the significant sound value over serial
    lastSpikeTime = millis();  // Update the time of the last detected spike
  } else {
    Serial.println(0);  // Print zero when no significant spike is detected
  }

  delay(50);  // Delay for 50 milliseconds before the next reading
}
