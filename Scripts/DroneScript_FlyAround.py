import Tello
import time
import sys

my_drone = Tello.Tello()
my_drone.streamon()

my_drone.takeoff()

# my_drone.up(75)
my_drone.forward(100)
my_drone.back(100)

for i in range(4):
    my_drone.cw(90)
    my_drone.forward(100)

time.sleep(0.5)
my_drone.up(50)
my_drone.land()
sys.exit(0)
