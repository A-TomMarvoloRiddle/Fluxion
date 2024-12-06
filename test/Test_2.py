import threading as t
from ultralytics import YOLO
model = YOLO("yolov10s.pt")
x=0
def capture_traffic_data(video_path):
    global x
    global model
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

def start_sys():
    t.Thread(target=capture_traffic_data, args=(video_path)).start()

def get_vc():
    global x
    return x
def get_mod():
    global model
    return model

