# Loads a video file.  Hit 'space' to save a frame.
import cv2

video_name = 'Drone_Flight_5'
cap = cv2.VideoCapture(video_name + '.mp4' )

if not cap.isOpened():
    print("Error opening video  file")

count = 0
ret = True
# Read until video is completed
while ret:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('space to capture', frame)
        if cv2.waitKey(40) & 0xFF == 32:
            file_name = video_name+ "_"  + str(count) + ".png"
            cv2.imwrite(file_name, frame)
            count += 1

