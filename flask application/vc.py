import time
import threading as t
import numpy as np
from ultralytics import YOLO

model1 = YOLO("yolov10s.pt")
model2 = YOLO("yolov10s.pt")
model3 = YOLO("yolov10s.pt")
model4 = YOLO("yolov10s.pt")

class TrafficLight:
    def __init__(self, direction):
        self.direction = direction
        self.state = "Red"  # Initial state
        self.duration = 0

    def set_state(self, state, duration=None):
        self.state = state
        self.duration = duration
        return (f">> {self.direction} >>> {self.state} >>> {self.duration} seconds"
                if self.state in ["Green", "Yellow"] else f"   {self.direction} >> {self.state} >> {self.duration} seconds")

    def get_state(self):
        return {
            'state': self.state,
            'duration': self.duration
        }

# Global variables
lights = {
    "north": TrafficLight("North"), 
    "south": TrafficLight("South"), 
    "east": TrafficLight("East"), 
    "west": TrafficLight("West")
}

traffic_data = {
    "north": 5, 
    "south": 25, 
    "east": 3, 
    "west": 16
}

# Locks and termination flag
traffic_data_lock = t.Lock()
lights_lock = t.Lock()
stop_event = t.Event()

def cap_traffic(direction, traffic_data, model):
    while not stop_event.is_set():
        predictions = model.predict(f"./{direction}.mp4", show=False, stream=True, classes=[1, 2, 3, 5, 7],
                                     vid_stride=10, conf=0.6, show_labels=True, line_width=2, verbose=False)
        for r in predictions:
            with traffic_data_lock:
                traffic_data[direction.lower()] = len(r.boxes)
            if stop_event.is_set():
                break
def gcurr():
    global traffic_data
    total_vehicles = sum(traffic_data.values()) + 20  # Add a baseline for calculations
    green_curr = []
    cumulative_red_time = 0  # Tracks the cumulative red time for prior directions

    for dir, count in traffic_data.items():
        count += 5  # Add a bias to the vehicle count
        if total_vehicles == 0:
            green_time = 8  # Default time when no vehicles
        else:
            # Calculate green time using logarithmic logic
            green_time = max(7, int(np.log(12.5 * 60 * (np.exp(count) // total_vehicles + 1))))
        yellow_time = 3  # Fixed yellow light duration

        red_time = cumulative_red_time

        cumulative_red_time += green_time + yellow_time

        green_curr.append([dir, green_time, red_time])
    
    return green_curr


def start_system():
    threads = [
        t.Thread(target=cap_traffic, args=("North", traffic_data, model1)),
        t.Thread(target=cap_traffic, args=("South", traffic_data, model2)),
        t.Thread(target=cap_traffic, args=("East", traffic_data, model3)),
        t.Thread(target=cap_traffic, args=("West", traffic_data, model4))
    ]

    for thread in threads:
        thread.start()

    time.sleep(10)
    stop_event.set()  # Signal threads to stop

    for thread in threads:
        thread.join()

    return gcurr()

if __name__ == "__main__":
    green_light_times = start_system()
    print("Green Light Times:", green_light_times)
