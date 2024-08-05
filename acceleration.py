import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)  
time.sleep(2)  

def read_throttle():
    ser.write(b'r')  
    time.sleep(0.1)  
    if ser.in_waiting > 0:
        throttle_value = ser.readline().decode().strip()
        return int(throttle_value)
    return None

def write_throttle(throttle_value):
    ser.write(b'w')  
    ser.write(str(throttle_value).encode() + b'\n')
    time.sleep(0.1)  

def main():
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
