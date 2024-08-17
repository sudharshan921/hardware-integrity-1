#include <Wire.h>
#include <Adafruit_MCP4725.h>

// Create an instance of the MCP4725 DAC
Adafruit_MCP4725 dac;

// Define the voltage levels for different speeds
const float voltages[] = {3.2, 3.6, 4.0, 4.4, 4.6};  // Adjust these based on your needs
const float speeds[] = {0, 7, 14, 18, 20};           // Corresponding speeds in km/h

const int REFERENCE_VOLTAGE = 5000;  // Reference voltage in millivolts
const int MIN_DAC_VALUE = 0;         // Minimum DAC value
const int MAX_DAC_VALUE = 4095;      // Maximum DAC value

void setup() {
  Serial.begin(9600);
  dac.begin(0x60);  // Initialize DAC with default I2C address (0x60)

  // Initialize throttle at a safe start voltage
  setThrottleVoltage(voltages[0]);
}

void loop() {
  // Example: Simulate speed changes
  for (int i = 0; i < sizeof(voltages) / sizeof(voltages[0]); i++) {
    setThrottleVoltage(voltages[i]);
    delay(2000);  // Wait for 2 seconds before moving to the next speed
  }

  delay(5000);  // Pause before restarting the cycle
}

// Function to set the throttle voltage safely
void setThrottleVoltage(float voltage) {
  // Convert voltage to DAC value
  uint16_t dacValue = calculateDACValue(voltage);

  // Check if DAC value is within range
  if (dacValue < MIN_DAC_VALUE || dacValue > MAX_DAC_VALUE) {
    Serial.println("ERROR: DAC value out of range. Halting.");
    emergencyShutdown();  // Call safety shutdown if out of range
    return;
  }

  // Send DAC value
  dac.setVoltage(dacValue, false);

  // Debug output
  Serial.print("Setting throttle to ");
  Serial.print(voltage);
  Serial.print("V (DAC Value: ");
  Serial.print(dacValue);
  Serial.println(")");
}

// Function to calculate the DAC value based on desired voltage
uint16_t calculateDACValue(float voltage) {
  return (uint16_t)((voltage * MAX_DAC_VALUE) / (REFERENCE_VOLTAGE / 1000.0));
}

// Optional safety shutdown function
void emergencyShutdown() {
  setThrottleVoltage(voltages[0]);  // Reset throttle to minimum voltage
  Serial.println("EMERGENCY SHUTDOWN ACTIVATED!");
  while (true);  // Halt execution indefinitely
}
