#an example of reading and processing the drone's video feed

import Tello
import ImageTools as IT

my_drone = Tello.Tello()

while True:
    frame = my_drone.get_frame()
    shade = IT.avg_color(frame, IT.GRAY)
    if shade > 100:
        print("light")
    else:
        print("dark")
