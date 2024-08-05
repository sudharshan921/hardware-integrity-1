import serial
import time

# Open serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port name as necessary
time.sleep(2)  # Wait for the serial connection to initialize

def read_throttle():
    ser.write(b'r')  # Send the 'r' command to read the throttle signal
    time.sleep(0.1)  # Wait for the Arduino to respond
    if ser.in_waiting > 0:
        throttle_value = ser.readline().decode().strip()
        return int(throttle_value)
    return None

def write_throttle(throttle_value):
    ser.write(b'w')  # Send the 'w' command to write the throttle signal
    ser.write(str(throttle_value).encode() + b'\n')
    time.sleep(0.1)  # Wait for the Arduino to process the command

def main():
    # Record throttle signal
    recorded_throttle_values = []
    print("Recording throttle signal. Press Ctrl+C to stop.")
    try:
        while True:
            throttle_value = read_throttle()
            if throttle_value is not None:
                recorded_throttle_values.append(throttle_value)
                print(f"Recorded throttle value: {throttle_value}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    
    print("Recording stopped.")
    
    # Use recorded throttle signal to control the car
    print("Replaying throttle signal. Press Ctrl+C to stop.")
    try:
        while True:
            for throttle_value in recorded_throttle_values:
                write_throttle(throttle_value)
                print(f"Throttle value set to: {throttle_value}")
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
