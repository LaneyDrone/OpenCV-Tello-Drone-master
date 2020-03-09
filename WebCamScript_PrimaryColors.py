import WebCam
import ImageTools as IT
import time

my_cam = WebCam.WebCam()
print("initialized")
my_cam.streamon()

while True:
    pass

while True:
    frame = my_cam.get_frame()
    red = IT.avg_color(frame, IT.RED)
    green = IT.avg_color(frame, IT.GREEN)
    blue = IT.avg_color(frame, IT.BLUE)
    print("red: " + str(red))
    print("green: " + str(green))
    print("blue: " + str(blue))
    print("the color is:")

    if blue > red and blue > green:
        print("blue!")
    elif red > blue and red > green:
        print("red!")
    elif green > blue and green > red:
        print("green!")
    else:
        print("I don't know")
    print()
    time.sleep(1)
