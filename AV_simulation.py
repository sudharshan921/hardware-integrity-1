import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
acceleration_rate = 2.0  # meters per second squared (m/s^2)
max_speed = 20.0 / 3.6  # converting km/h to m/s
duration = 10.0  # seconds to maintain max speed
deceleration_rate = 2.0  # meters per second squared (m/s^2)

# Initial speed
current_speed = 0.0

# Time interval for the control loop
time_interval = 0.1  # seconds

# Lists to store time and speed for plotting
time_list = []
speed_list = []

# Lists to store car position and speed for animation
position_list = []
car_speed_list = []

# Function to update vehicle speed
def update_speed(speed):
    global current_speed
    current_speed = speed

# Phase 1: Acceleration
while current_speed < max_speed:
    current_speed += acceleration_rate * time_interval
    if current_speed > max_speed:
        current_speed = max_speed
    update_speed(current_speed)
    time_list.append(time.time())
    speed_list.append(current_speed)
    if position_list:
        position_list.append(position_list[-1] + current_speed * time_interval)
    else:
        position_list.append(current_speed * time_interval)
    car_speed_list.append(current_speed * 3.6)  # convert to km/h for display
    time.sleep(time_interval)

# Phase 2: Maintain max speed
start_time = time.time()
while (time.time() - start_time) < duration:
    update_speed(max_speed)
    time_list.append(time.time())
    speed_list.append(current_speed)
    position_list.append(position_list[-1] + current_speed * time_interval)
    car_speed_list.append(current_speed * 3.6)  # convert to km/h for display
    time.sleep(time_interval)

# Phase 3: Deceleration
while current_speed > 0:
    current_speed -= deceleration_rate * time_interval
    if current_speed < 0:
        current_speed = 0
    update_speed(current_speed)
    time_list.append(time.time())
    speed_list.append(current_speed)
    position_list.append(position_list[-1] + current_speed * time_interval)
    car_speed_list.append(current_speed * 3.6)  # convert to km/h for display
    time.sleep(time_interval)

# Convert time_list to relative time
initial_time = time_list[0]
relative_time_list = [t - initial_time for t in time_list]

# Convert speeds from m/s to km/h for plotting
speed_list_kmh = [speed * 3.6 for speed in speed_list]

# Plot the speed graph
plt.figure(figsize=(10, 5))
plt.plot(relative_time_list, speed_list_kmh, label='Vehicle Speed (km/h)')
plt.xlabel('Time (s)')
plt.ylabel('Speed (km/h)')
plt.title('Vehicle Speed Simulation')
plt.legend()
plt.grid(True)
plt.show()

# Create figure and axis for animation
fig, ax = plt.subplots()
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)

# Rectangle representing the car
car = plt.Rectangle((0, 0.4), 3, 0.1, fc='blue')
ax.add_patch(car)

# Text for displaying speed
speed_text = ax.text(0.05, 0.85, '', transform=ax.transAxes)

# Function to update the animation
def animate(i):
    car.set_x(position_list[i])
    speed_text.set_text(f'Speed: {car_speed_list[i]:.2f} km/h')
    return car, speed_text

# Function to start the animation after a delay
def delayed_start():
    plt.pause(3)  # Delay before starting the animation
    ani.event_source.start()

# Create the animation
ani = FuncAnimation(fig, animate, frames=len(relative_time_list), interval=time_interval*1000, blit=True, repeat=False)

# Start the animation after a delay
delayed_start()

plt.show()
