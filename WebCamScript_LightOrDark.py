#An example of interfacing with the live video feed from your webcam

import WebCam
import ImageTools as IT
import time

my_cam = WebCam.WebCam()
print("initialized")
my_cam.streamon()

while True:
    frame = my_cam.get_frame()
    shade = IT.avg_color(frame, IT.GRAY)
    if shade > 100:
        print("light")
    else:
        print("dark")
        
