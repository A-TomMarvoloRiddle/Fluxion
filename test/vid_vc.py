import threading as t
from ultralytics import YOLO
import random
#model = YOLO("yolov10s.pt")
x=0
def capture_traffic_data(model,video_path):
    global x
    predictions = model.predict(
        video_path,
        show=False,
        stream=True,
        classes=[1, 2, 3, 5, 7],
        vid_stride=10,
        conf=0.6,
        show_labels=True,
        verbose=False,
    )
    for result in predictions:
        x= len(result.boxes)

def start_sys(vid_path):
    #f"model{i}" = YOLO("yolov10s.pt")
    t.Thread(target=capture_traffic_data, args=(YOLO("yolov10s.pt"),vid_path)).start()

def get_vc():
    global x
    return 2*random.randint(5,20)
