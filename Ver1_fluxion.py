import time
import threading as t
import numpy as np
from ultralytics import YOLO
import torch
print("Is CUDA GPU available: ",torch.cuda.is_available())
# Load YOLO models
models = {
    "north": YOLO("yolov10s.pt"),
    "south": YOLO("yolov10s.pt"),
    "east": YOLO("yolov10s.pt"),
    "west": YOLO("yolov10s.pt"),
}

# Traffic light class
class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = "Red"  # Initial state
        self.duration = 0  # Initial duration

    def set_state(self, state, duration=None):
        self.state = state
        self.duration = duration
        print(
            f">> {self.direction} >>> {self.state} >>> {self.duration} seconds" if self.state in ["Green", "Yellow"] else f"   {self.direction} >> {self.state} >> {self.duration} seconds")

# Initialize traffic lights
lights = {dir: TrafficLight(dir.capitalize()) for dir in models.keys()}

# Traffic data for each direction
traffic_data = {dir: 5 for dir in models.keys()}

def capture_traffic_data(direction, model, video_path, traffic_data):
    predictions = model.predict(
        video_path,
        show=True,
        stream=True,
        classes=[1, 2, 3, 5, 7],
        vid_stride=10,
        conf=0.6,
        show_labels=True,
        verbose=False,
    )
    for result in predictions:
        traffic_data[direction] = len(result.boxes)

def calculate_green_time(traffic_data):
    """Calculate the green time for each direction."""
    total_vehicles = sum(traffic_data.values()) + 20
    green_times = []
    print(f"\nTotal Vehicles: {total_vehicles}\n")

    for direction, count in traffic_data.items():
        count += 5
        print(f"{direction.capitalize()}: {count}")
        green_time = max(7, int(np.log(12.5 * 60 * (np.exp(count) // (total_vehicles + 1)))))
        green_times.append([direction, green_time, 0])

    print(f"\nGreen Times: {green_times}\n")
    return green_times

def calculate_red_times(green_times):
    """Calculate the red time for each direction."""
    for i in range(1, len(green_times)):
        green_times[i][2] = sum(green_times[j][1] + 5 for j in range(i))
    return green_times

def change_lights(lights, final_schedule):
    """Change lights based on the calculated schedule."""
    while final_schedule:
        print(f"\nFinal Schedule: {final_schedule}\n")
        current = final_schedule[0]
        next_directions = final_schedule[1:4]

        # Set green light for current direction
        lights[current[0]].set_state("Green", current[1])
        for dir in next_directions:
            lights[dir[0]].set_state("Red", dir[2])

        time.sleep(current[1])

        # Set yellow light for current direction
        lights[current[0]].set_state("Yellow", 5)
        for dir in next_directions:
            dir[2]=dir[2]-current[1]
            lights[dir[0]].set_state("Red", dir[2])

        time.sleep(5)

        # Rotate the schedule and update red times
        final_schedule.pop(0)
        final_schedule = calculate_red_times(final_schedule)

        # Add new green time schedule every cycle
        if current[0] == "north":
            final_schedule.extend(calculate_green_time(traffic_data))
            final_schedule = calculate_red_times(final_schedule)

def start_traffic_system(video_paths):
    """Start the traffic management system."""
    print("\n       FLUXION by ERROR 404\n")

    # Capture real-time traffic data
    for direction, video_path in video_paths.items():
        t.Thread(target=capture_traffic_data, args=(direction, models[direction], video_path, traffic_data)).start()

    time.sleep(10)  # Allow time for initial data capture

    # Calculate initial green and red times
    schedule = calculate_green_time(traffic_data)
    schedule = calculate_red_times(schedule)

    # Start the automated system
    t.Thread(target=change_lights, args=(lights, schedule)).start()

# Video paths for each direction
video_paths = {
    "north": "D:/North.mp4",
    "south": "D:/South.mp4",
    "east": "D:/East.mp4",
    "west": "D:/West.mp4",
}

# Start the system
start_traffic_system(video_paths)