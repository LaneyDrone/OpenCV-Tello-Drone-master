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
my_drone.wait(10)
print(my_drone.get_height())
my_drone.down(20)
my_drone.wait(5)
my_drone.land()
sys.exit(0)
