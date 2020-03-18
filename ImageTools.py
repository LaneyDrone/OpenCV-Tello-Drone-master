import cv2
import numpy as np
import FunTools as FT
import statistics as stats


def load_image(filename):
    return cv2.imread(filename)


def display_image(img):
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def load_video(file_name):
    return cv2.VideoCapture(file_name)


def display_video(video):
    count = 0
    ret = True
    # Read until video is completed
    while ret:
        ret, frame = video.read()
        if ret:
            cv2.imshow('space to capture', frame)
            k = cv2.waitKey(40) & 0xFF
            if k  == 32:
                file_name = 'video_capture' + "_" + str(count) + ".png"
                cv2.imwrite(file_name, frame)
                count += 1
            elif k == 27:
                break
                cap.release()
                cv2.destroyAllWindows()



# Converts an image to grayscale
def convert_to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Assumes img is already in gray_scale
def average_gray_value(img):
    flattened_image = np.ravel(img)
    return stats.mean(flattened_image)


# This downsamples by taking every fourth pixel.
# There is a better way to do this.
def downsample(img):
    num_rows = img.shape[0]
    num_cols = img.shape[1]
    downsampled_image = []
    current_row = []
    for row in range(1, num_rows, 4):
        for col in range(1, num_cols, 4):
            current_row.append(img[row, col])
        downsampled_image.append(current_row)
        current_row = []
    return np.array(downsampled_image)


# Returns the coordinates of edges in the image
# Note that images are represented by matrices, which are indexed by coordinates of the form (row,col)
# So if (50,100) is in edge_coordinates, the corresponding (x,y) point is (100,50).
# Also note that for images, (0,0) is the top left corner.  Moving down increases y-coordinates, so
# (0,1) is BELOW (0,0)
def get_edge_coordinates(img):
    img = cv2.medianBlur(img, 5)
    img = convert_to_grayscale(img)
    if average_gray_value(img) < 128:
        img = cv2.bitwise_not(img)
    ret, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    cv2.imwrite('current_edges.png', edges)
    rows = range(edges.shape[0])
    cols = range(edges.shape[1])
    edge_coordinates = []
    for row in rows:
        for col in cols:
            if edges[row, col] == 255:
                edge_coordinates.append([row, col])
    return edge_coordinates


# Feturns two dictionaries in a list
# For col_dict, the keys are the rows and the entries are the columns of all edge coordinates with the first entry = key
# E.g. If edge_coordinates = [[1, 100], [1, 200], [2, 300], [2, 400], ...],
# then, col_dict[1] = [100, 200], and col_dict[2] = [300,400]

# row_dict is the dual of col_dict.  The keys are columns
# E.g. if edge_coordinates = [[1, 100], [2, 100], [3, 200], [4, 200]]
# then, row_dict[100] = [1,2] and row_dict[200] = [3,4]
def make_dicts(edge_coordinates):
    col_dict = {}
    row_dict = {}
    for coord in edge_coordinates:
        if not coord[0] in col_dict:
            col_dict[coord[0]] = [coord[1]]
        else:
            to_add = col_dict[coord[0]]
            to_add.append(coord[1])
            col_dict[coord[0]] = to_add

        if not coord[1] in row_dict:
            row_dict[coord[1]] = [coord[0]]
        else:
            to_add = row_dict[coord[1]]
            to_add.append(coord[0])
            row_dict[coord[1]] = to_add
    return [row_dict, col_dict]


# line starts with a single [row,col] coordinate.
# the method then looks for an edge_coordinate of the form [row + 1, col -1] , [row + 1, col] or [row + 1, col + 1]
# if none are found, the vertical line is finished.
# Otherwise, the process is repeated until we have a list of all coordinates making up the vertical line
# Note.  Occasionally there are vertical lines where the column jumps by 2 pixels.
# If this turns out to be a problem, this will need to be fixed.
#
# Python has a recursion depth of 1,000.  The recursive version of make_vertical_line runs slightly faster than the
# iterative version, but will not find lines longer than 1,000 pixels.  If this is a problem, use make_vertical_line_i,
# the iterative version of this function
def make_vertical_line(col_dict, line, count):
    seed = line[-1]
    next_row = seed[0] + 1
    if not next_row in col_dict or count == 999:
        return line
    else:
        next_col_list = FT.filter(lambda c: abs(c - seed[1]) < 2, col_dict[next_row])
        if len(next_col_list) == 0:
            return line
        else:
            line.append([next_row, next_col_list[0]])
            return make_vertical_line(col_dict, line, count + 1)


def make_vertical_line_i(col_dict, line):
    seed = line[0]
    next_row = seed[0] + 1
    if next_row in col_dict:
        next_col_list = FT.filter(lambda c: abs(c - seed[1]) < 2, col_dict[next_row])
    while (next_row in col_dict) and (len(next_col_list) > 0):
        next_col_list = FT.filter(lambda c: abs(c - seed[1]) < 2, col_dict[next_row])
        line.append([next_row, next_col_list[0]])
        seed = line[-1]
        next_row = seed[0] + 1
        if next_row in col_dict:
            next_col_list = FT.filter(lambda c: abs(c - seed[1]) < 2, col_dict[next_row])
    return line


# Almost the same as make_vertical_line with the obvious swap with "row" and "col"
def make_horizontal_line(row_dict, line, count):
    seed = line[-1]
    next_col = seed[1] + 1
    if not next_col in row_dict or count == 999:
        return line
    else:
        next_col_list = FT.filter(lambda c: abs(c - seed[0]) < 2, row_dict[next_col])
        if len(next_col_list) == 0:
            return line
        else:
            line.append([next_col_list[0], next_col])
            return make_horizontal_line(row_dict, line, count  + 1)

def make_horizontal_line_i(row_dict, line):
    seed = line[0]
    next_col = seed[1] + 1
    if next_col in row_dict:
        next_col_list = FT.filter(lambda c: abs(c - seed[0]) < 2, row_dict[next_col])
    while (next_col in row_dict) and (len(next_col_list) > 0):
        line.append([next_col_list[0], next_col])
        seed = line[-1]
        next_col = seed[1] + 1
        if next_col in row_dict:
            next_col_list = FT.filter(lambda c: abs(c - seed[0]) < 2, row_dict[next_col])
    return line


# returns a list with the first entry a list of all horizontal lines, the second all vertical lines
# each line consists of a list of coordinates in order.
# both line lists are sorted by length.  The longest lines are listed first.
def get_lines(img):
    edge_coordinates_for_verticals  = get_edge_coordinates(img)
    edge_coordinates_for_horizontals = list(edge_coordinates_for_verticals) #faster if we copy this
    dicts =  make_dicts(edge_coordinates_for_verticals)
    edge_coordinates_for_verticals .sort(key=lambda x: x[0])
    edge_coordinates_for_horizontals.sort(key=lambda x: x[1])

    row_dict = dicts[0]
    col_dict = dicts[1]

    horizontal_lines = []
    vertical_lines = []

    while len(edge_coordinates_for_horizontals) > 0:
        current_seed = edge_coordinates_for_horizontals[0]
        # current_line = make_horizontal_line_i(row_dict, [current_seed])
        current_line = make_horizontal_line(row_dict, [current_seed], 0)
        horizontal_lines.append(current_line)
        edge_coordinates_for_horizontals = FT.remove_from_list(edge_coordinates_for_horizontals, current_line)

    while len(edge_coordinates_for_verticals) > 0:
        current_seed = edge_coordinates_for_verticals[0]
        # current_line = make_vertical_line_i(col_dict, [current_seed])
        current_line = make_vertical_line(col_dict, [current_seed], 0)
        vertical_lines.append(current_line)
        edge_coordinates_for_verticals = FT.remove_from_list(edge_coordinates_for_verticals, current_line)

    horizontal_lines.sort(key = len, reverse = True)
    vertical_lines.sort(key=len, reverse = True)
    return [horizontal_lines, vertical_lines]
