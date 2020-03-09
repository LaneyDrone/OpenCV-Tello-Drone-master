# Basic tools to process images. This will need many more functions
import cv2

BLUE = 0
GREEN = 1
RED = 2
GRAY = 3

def get_color_channel(frame, color):
    return frame[:, :, color]

def avg_color(frame, color):
    if color == GRAY:
        frame_channel = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        frame_channel = frame[:, :, color]

    num_rows = len(frame_channel[:, 0])
    num_columns = len(frame_channel[0, :])
    local_sum = 0
    for row in (range(num_rows)):
        for col in (range(num_columns)):
            local_sum = local_sum + frame_channel[row, col]
    return local_sum / (num_rows * num_columns)

def load_image(file_name):
    return cv2.imread(file_name)
