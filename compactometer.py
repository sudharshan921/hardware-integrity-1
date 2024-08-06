import serial
import time
import csv

# Set the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's port

def read_sound_sensor_data():
    ser.flushInput()
    with open('sound_data_log.csv', 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Sound Level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            try:
                # Read the serial data
                serial_line = ser.readline().decode('utf-8').strip()
                if serial_line:
                    sound_value = int(serial_line)
                    timestamp = time.time()
                    print(f"Timestamp: {timestamp}, Sound Level: {sound_value}")

                    # Log data to CSV
                    writer.writerow({'Timestamp': timestamp, 'Sound Level': sound_value})
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    time.sleep(2)  # Wait for Arduino to reset
    read_sound_sensor_data()
