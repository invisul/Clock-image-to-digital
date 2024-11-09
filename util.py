import cv2
import numpy as np


# HELPER FUNCTION

# helper function that receives input time in the form of a string in the following format "HH:MM"
# HH stands for hours
# MM stand for minutes
# returns the hours, minutes in int if the input is valid
def parse_string_time_input(time_input):
    try:
        time_input = time_input.split(":")
        if len(time_input) != 2:
            print("Time input is invalid, can't draw")
            exit()
        try:
            time_input_as_int = [int(number) for number in time_input]
            if time_input_as_int[0] > 24 or time_input_as_int[0] < 0:
                print(f"Hours input {time_input_as_int[0]} is invalid please enter a value between 24 and 0")
                exit()
            if time_input_as_int[1] > 59 or time_input_as_int[1] < 0:
                print(f"input {time_input_as_int[0]}:{time_input_as_int[1]} is invalid please enter minutes value between 59 and 0")
                exit()
        except Exception as e:
            print("Input is not a valid clock time, please try again")
            exit()
        # if we got here than we have a valid time.
    except ValueError:
        print(f"unknown error has occured while parsing {time_input}")
    return time_input_as_int[0] % 12, time_input_as_int[1]


# HELPER FUNCTION

# The function returns the x,y values of the middle of the circle if found one. and its radius.
# The function uses openCV function HoughCircles to find the circle and its center.
def find_circle_center(image, debug):
    #  needed to blurr twice for accurate result. need to understand why
    img = cv2.medianBlur(image, 5)
    img = cv2.medianBlur(img, 3)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 200,
                              param1=70, param2=20, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.round(circles[0, :]))
        # Assuming the largest circle detected is the clock face
        x, y, r = circles[0]
        if debug:
            cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            # draw the outer circle
            cv2.circle(cimg, (x, y), r, (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (x, y), 2, (0, 0, 255), 3)
            cv2.imshow('detected circles', cimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return (x, y), r
    else:
        raise ValueError("No clock face found.")


# HELPER FUNCTION

# Function receives the image, and returns the lines found by openCV's HoughLinesP algorithm.
# if debug mode is activated, will print the image with the addition of the lines found.
def find_lines(image, debug):
    edges = cv2.Canny(image, 50, 150)

    # Use the Hough method to find straight lines from the edges
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=40, minLineLength=50, maxLineGap=5)
    if debug:
        color_layer = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(color_layer, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.imshow("find lines", color_layer)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    return lines


# HELPER FUNCTION

# function that receives the center of the circle, the line we want to calculate and performed the following calculation
#  treats the center as the vector (0, -1) which is  pointing to 12 for convenience
#  performs dot between the 2 vectors and uses it to calculate the angle.
def calculate_angle(center, line):
    x1, y1, x2, y2 = line
    dx, dy = x2 - center[0], y2 - center[1]
    up = (0, -1)
    dot = np.dot(up, (dx, dy))

    cos_angle = dot / (np.linalg.norm((dx, dy)))

    angle = np.degrees(np.acos(cos_angle))
    # fix according to cosine
    if dx < 0:
        angle = 360 - angle
    return angle


# HELPER FUNCTION
# function to call angle calculations for each hand, hours nad minutes and returns the result
def find_hand_angles(hour_line, minute_line, center):
    # getting the angles for both hours and minutes
    hour_angle = calculate_angle(center, hour_line)
    minute_angle = calculate_angle(center, minute_line)
    return hour_angle, minute_angle


# HELPER FUNCTION
# checks if given line is close to the center of the circle. with allowed variance of 10%
# this is to prevent the case that HoughLinesP algorithm from openCV finds a line that is not one of the clock hands
def line_starts_near_center(line, center, tolerance=0.1):
    # check if one the line edges is near the center of the clock.
    x1, y1, x2, y2 = line
    centerx, centery = center
    if abs(x1 - centerx) <= centerx * tolerance and abs(y1 - centery) <= centery * tolerance:
        return True
    elif abs(x2 - centerx) <= centerx * tolerance and abs(y2 - centery) <= centery * tolerance:
        return True
    return False


# HELPER FUNCTION
# The function receives the lines and center of the circle.
# returns the long line as the minutes hand and the shorter one as the horus hand while ignoring lines that are irrelevant
# TODO might needs to be improve incase of a short line that is pretty close and found inside of another line
def organize_lines(lines, center):
    max_length = 0
    minute_hand = None
    hour_hand = None

    for line in lines:
        line = line.squeeze()
        if not line_starts_near_center(line,center):
            continue
        x1, y1, x2, y2 = line

        # move the values so that the location line[3] representing
        # since the lines are generated as (x1, y1, x2, y2) with x1 having the lower x value.
        # in order to make sure that we handle it correctly. we shift between the value incase of y1 is bigger.
        # to  match the behavior of cosine
        if abs(y1 - center[1]) > center[1] * 0.1:
            line[0] = x2
            line[1] = y2
            line[2] = x1
            line[3] = y1
        length = np.hypot(x2 - x1, y2 - y1)
        if length > max_length:
            # Longer line is more likely to be the minute hand
            if minute_hand is not None:
                hour_hand = minute_hand  # Reassign the previous longest as hour hand
            minute_hand = line
            max_length = length
        elif hour_hand is None or length < max_length * 0.9:
            hour_hand = line
    return hour_hand, minute_hand