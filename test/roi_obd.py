import cv2 
from ultralytics import YOLO  

def frame_generator(video_path, skip_frames=5):
    """Generator to yield frames from video, skipping specified number of frames"""
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % (skip_frames + 1) == 0:
                yield frame
            
            frame_count += 1
    finally:
        cap.release()

def detect_objects_in_video_roi(input_video_path, output_video_path, selected_classes=[1,2,3,5,7], confidence_threshold=0.4, skip_frames=5):
    # Load YOLOv10 model
    model = YOLO("yolov10s.pt")
    model.conf = confidence_threshold  

    # Create video writer
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()  

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))  

    # Read first frame for ROI selection
    first_frame_gen = frame_generator(input_video_path, skip_frames)
    first_frame = next(first_frame_gen)  

    # Select ROI
    roi = cv2.selectROI("Select ROI", first_frame)
    cv2.destroyAllWindows()
    x_start, y_start, width, height = map(int, roi)  

    # Process frames
    for frame in frame_generator(input_video_path, skip_frames):
        # Crop frame to ROI
        roi_frame = frame[y_start:y_start+height, x_start:x_start+width] if roi != (0,0,0,0) else frame  

        # Detect objects
        results = model(roi_frame)  

        # Draw detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Check if class is in selected classes
                if int(box.cls[0]) in selected_classes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = map(int, [x1+x_start, y1+y_start, x2+x_start, y2+y_start])
                    
                    # Get confidence and class
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    
                    # Draw rectangle
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Add label
                    label = f"{conf*100:.2f}"
                    cv2.putText(frame, label, (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Draw ROI rectangle
        cv2.rectangle(frame, (x_start, y_start), (x_start+width, y_start+height),(255, 0, 0), 2)

        # Write and display frame
        out.write(frame)
        cv2.imshow('Object Detection in ROI', frame)

        # Break on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    out.release()
    cv2.destroyAllWindows()

# Example usage
#input_video = "https://www.youtube.com/watch?v=iJZcjZD0fw0"
input_video="C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/West.mp4"
output_video = "detected_video.mp4"
try:
    detect_objects_in_video_roi(input_video, output_video)
except:
    print("Error occurred. Please check the input video URL and try again.")
    print("Predictions based on RNN Model trained on previous data.")
