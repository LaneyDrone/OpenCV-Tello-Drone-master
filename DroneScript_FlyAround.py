# an example of sending commands to the drone

import Tello
import time
import sys

my_drone = Tello.Tello()
my_drone.streamon()

my_drone.takeoff()
time.sleep(2)
print(my_drone.get_height())

# my_drone.up(75)
my_drone.down(20)
my_drone.wait(5)
print(my_drone.get_height())
my_drone.forward(100)

"""
#update check -- could be included too

my_drone.back(100)

for i in range(4):
    my_drone.cw(90)
    my_drone.forward(100)

time.sleep(0.5)
my_drone.up(50)
"""

my_drone.wait(10)
print(my_drone.get_height())
my_drone.down(20)
my_drone.wait(5)
my_drone.land()
sys.exit(0)
