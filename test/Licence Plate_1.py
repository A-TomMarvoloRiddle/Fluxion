import cv2
import numpy as np

# Load the plate detector cascade
plat_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

# Load the video file
video = cv2.VideoCapture("C:/Users/Apaar/Pictures/FLUXION/Data_Aryan/WhatsApp Video 2024-12-12 at 11.47.19_dada3d43.mp4")

if not video.isOpened():
    print('Error Reading Video')
    exit()

# List to store detected plates
detected_plates = []

while True:
    ret, frame = video.read()
    
    if not ret:
        break  # Break the loop if video ends
    gray_video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    plates = plat_detector.detectMultiScale(gray_video, scaleFactor=1.2, minNeighbors=5, minSize=(25, 25))

    for (x, y, w, h) in plates:
        # Draw a rectangle around the plate
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # Label the plate
        cv2.putText(frame, text='License Plate', org=(x - 3, y - 3), fontFace=cv2.FONT_HERSHEY_COMPLEX,
                    color=(0, 0, 255), thickness=1, fontScale=0.6)
        
        # Crop and save the detected plate
        plate_img = frame[y:y + h, x:x + w]
        detected_plates.append(plate_img)

    # Display the video frame
    cv2.imshow('Video', frame)

    # Break on 'q' key press
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

# Release the video and close all OpenCV windows
video.release()
cv2.destroyAllWindows()

# Example: Save all detected plates as images
for idx, plate in enumerate(detected_plates):
    cv2.imwrite(f'detected_plate_{idx}.jpg', plate)
