# Hold something white up to your webcam.  Notice the output.  Now hold up something black.

import WebCam
import ImageTools as IT
import time

my_cam = WebCam.WebCam()
my_cam.streamon()

while True:
    frame = my_cam.get_frame()
    shade = IT.average_gray_value(frame)
    if shade > 100:
        print("light")
    else:
        print("dark")
