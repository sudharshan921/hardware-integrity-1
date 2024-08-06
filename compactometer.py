import serial
import csv
import time

# Set the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's port

def read_accelerometer_data():
    csv_file = 'accelerometer_data.csv'
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Timestamp', 'X', 'Y', 'Z'])

        while True:
            try:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()
                # Split the line into components
                if line:
                    data = line.split()
                    if len(data) == 6:  # Adjust according to your serial output format
                        timestamp = time.time()
                        x = float(data[1].replace("X:", ""))  # Ensure data is correctly converted to float
                        y = float(data[3].replace("Y:", ""))
                        z = float(data[5].replace("Z:", ""))

                        # Write the data to the CSV file
                        writer.writerow([timestamp, x, y, z])
                        print(f"Timestamp: {timestamp}, X: {x}, Y: {y}, Z: {z}")

            except KeyboardInterrupt:
                print("Exiting accelerometer data logging...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

def read_sound_sensor_data():
    csv_file = 'sound_data_log.csv'
    with open(csv_file, 'w', newline='') as csvfile:
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
            except KeyboardInterrupt:
                print("Exiting sound sensor data logging...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    time.sleep(2)  # Wait for Arduino to reset
    while True:
        try:
            read_accelerometer_data()
            read_sound_sensor_data()
        except KeyboardInterrupt:
            print("Exiting...")
            break

# Close the serial connection
ser.close()

