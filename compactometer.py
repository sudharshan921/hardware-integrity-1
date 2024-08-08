import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class CompactometerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compactometer Simulation")
        self.root.geometry("800x600")  # Increase the size of the window

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Canvas(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas_frame.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas_frame.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_frame.bind('<Configure>', lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all")))

        self.graph_frame = tk.Frame(self.canvas_frame)
        self.canvas_frame.create_window((0, 0), window=self.graph_frame, anchor="nw")

        self.vibration_label = tk.Label(self.graph_frame, text="Vibration Level: 0", font=("Arial", 16), bg='#1b1b1b', fg='#ffffff')
        self.vibration_label.pack(pady=20)

        self.status_label = tk.Label(self.graph_frame, text="Status: Not Started", font=("Arial", 16), bg='#1b1b1b', fg='#ffffff')
        self.status_label.pack(pady=20)

        self.start_button = tk.Button(self.graph_frame, text="Start Simulation", command=self.start_simulation, font=("Arial", 16), bg='#4CAF50', fg='#ffffff')
        self.start_button.pack(pady=20)

        self.hike_threshold = 2.0
        self.hike_count = 0
        self.hike_detected = False
        self.cycle_count = 0
        self.vibration_on = False
        self.current_direction = 'forward'
        self.start_time = None

        # Data storage for each pass
        self.passes = []

    def start_simulation(self):
        self.status_label.config(text="Status: Simulating...")
        self.hike_count = 0
        self.hike_detected = False
        self.cycle_count = 0
        self.vibration_on = False
        self.current_direction = 'forward'
        self.start_time = datetime.now()
        self.passes = []  # Clear previous passes
        self.simulate_vibration()

    def add_new_graph(self):
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#1b1b1b')
        ax.set_facecolor('#2b2b2b')
        ax.spines['bottom'].set_color('#ffffff')
        ax.spines['top'].set_color('#ffffff')
        ax.spines['right'].set_color('#ffffff')
        ax.spines['left'].set_color('#ffffff')
        ax.tick_params(axis='x', colors='#ffffff')
        ax.tick_params(axis='y', colors='#ffffff')
        ax.xaxis.label.set_color('#ffffff')
        ax.yaxis.label.set_color('#ffffff')
        ax.title.set_color('#ffffff')
        ax.set_title(f"Vibration Waveform - Pass {self.cycle_count + 1}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Vibration Level")

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=20)

        # Update scroll region to include the new graph
        self.canvas_frame.update_idletasks()
        self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))

        return fig, ax

    def simulate_vibration(self):
        if self.hike_count >= 5 and self.cycle_count >= 6:
            self.status_label.config(text="Status: Compaction Complete")
            self.vibration_label.config(text="Vibration Level: 0")
            return

        current_time = (datetime.now() - self.start_time).total_seconds()

        base_amplitude = 0.5 if self.cycle_count == 0 else 1.0 if self.vibration_on else 0.5

        if self.current_direction == 'forward':
            self.vibration_on = self.cycle_count > 0 and self.cycle_count <= 5
            if self.vibration_on:
                base_amplitude = 1.5
        else:
            self.vibration_on = False
            base_amplitude = 0.5

        frequency_variation = np.random.normal(0, 2)
        amplitude_variation = np.random.normal(0, 0.2)
        noise = np.random.normal(0, 0.1)

        frequency = 10 + frequency_variation
        amplitude = base_amplitude + amplitude_variation

        vibration = amplitude * np.sin(2 * np.pi * frequency * current_time) + noise

        if self.vibration_on and self.cycle_count >= 5:
            if np.random.rand() > 0.95:
                vibration += 2.0
                self.hike_detected = True

        if self.hike_detected and abs(vibration) > self.hike_threshold:
            self.hike_count += 1
            self.hike_detected = False

        self.vibration_label.config(text=f"Vibration Level: {vibration:.2f}")

        if len(self.passes) <= self.cycle_count:
            self.passes.append({
                'time': [],
                'forward': [],
                'backward': []
            })

        if self.current_direction == 'forward':
            self.passes[self.cycle_count]['time'].append(current_time)
            self.passes[self.cycle_count]['forward'].append(vibration)
            self.passes[self.cycle_count]['backward'].append(None)  # Placeholder for backward data
        else:
            self.passes[self.cycle_count]['time'].append(current_time)
            self.passes[self.cycle_count]['forward'].append(None)  # Placeholder for forward data
            self.passes[self.cycle_count]['backward'].append(vibration)

        if not hasattr(self, 'current_ax'):
            self.current_fig, self.current_ax = self.add_new_graph()

        # Clear current axis
        self.current_ax.clear()

        # Plot data for current pass
        pass_data = self.passes[self.cycle_count]
        self.current_ax.plot(pass_data['time'], pass_data['forward'], label='Forward', color='blue', linewidth=2)
        self.current_ax.plot(pass_data['time'], pass_data['backward'], label='Backward', color='red', linewidth=2)
        self.current_ax.set_title(f"Vibration Waveform - Pass {self.cycle_count + 1}")
        self.current_ax.set_xlabel("Time (s)")
        self.current_ax.set_ylabel("Vibration Level")
        self.current_ax.legend()
        self.current_fig.canvas.draw()

        if current_time > 20:  # End of pass, switch direction or create a new graph
            if self.current_direction == 'backward':
                self.cycle_count += 1
                self.current_fig, self.current_ax = self.add_new_graph()
            self.current_direction = 'backward' if self.current_direction == 'forward' else 'forward'
            self.start_time = datetime.now()

        # Ensure the scroll region is updated dynamically
        self.canvas_frame.update_idletasks()
        self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))

        self.root.after(20, self.simulate_vibration)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#1b1b1b')
    app = CompactometerApp(root)
    root.mainloop()

