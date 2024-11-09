import pygame
import time
import math
import sys
import cv2
from os.path import exists
import numpy as np
import argparse
from random import randint

input_active_color = pygame.Color('white')
debug = False


# Class to enable addition of more buttons to pygame
class Button:
    def __init__(self, rect, text, font, color, text_color):
        self.rect = rect
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
        self.is_clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_clicked(self, event):
        if event is None or not isinstance(event, pygame.event.EventType):
            print("Invalid event sent to check_clicked")
            return False

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
        self.is_clicked = self.rect.collidepoint(event.pos)
        return self.is_clicked


# Class to display the clock when receiving digital time as input
class ClockDisplay:

    def __init__(self, width, height):
        pygame.init()
        if width <= 0 or width > 5000:
            print("Screen width is invalid. please choose a value between 5000 and 0")
        if height <= 0 or height > 600:
            print("Screen height is invalid. please choose a value between 600 and 0")

        pygame.display.set_caption("Analog and Digital Clock with Set Time")
        self.screen = pygame.display.set_mode((width, height))
        # added random variable to the location to make clock abit different each time
        # self.center = (width // 2 + randint(-50, 50), height//2 + randint(-50, 50))
        self.center = (width // 2, height//2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)
        # self.circle_size = randint(160, 250)
        self.circle_size = 200

        button_font = pygame.font.Font(None, 24)
        button_color = pygame.Color('blue')
        button_text_color = pygame.Color('white')
        self.exitButton = Button(pygame.Rect(width // 3 - self.circle_size, 460, 100, 40), "Close",  button_font, button_color, button_text_color)

    def __del__(self):
        pygame.quit()

    def generate_clock_image(self, hours, minutes):
        # drawing the clock circle with markers for hours
        # creating a white screen
        self.screen.fill((255, 255, 255))
        # Generate a unique filename with the current date and time
        timestamp = time.time()
        filename = f"clock_{timestamp}.png"
        # drawing the clock itself (the circle)
        self.draw_clock_face()

        # calculating the angles of the pointers
        hour_angle, minute_angle = self.calculate_hand_angles(hours, minutes)

        # drawing the pointers for hours and minutes
        self.draw_hand(80, hour_angle, (0, 0, 0), 8)
        self.draw_hand(120, minute_angle, (0, 0, 0), 8)

        # Save the current screen as a PNG image
        pygame.image.save(self.screen, filename)
        print(f"Clock image saved as {filename}")
        return filename

    def draw_clock_face(self):
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.circle_size, 3)
        for hour in range(12):
            angle = np.radians(hour * 30)
            start_x = self.center[0] + (self.circle_size - 5) * np.cos(angle)
            start_y = self.center[1] + (self.circle_size - 5) * np.sin(angle)
            end_x = self.center[0] + self.circle_size * np.cos(angle)
            end_y = self.center[1] + self.circle_size * np.sin(angle)
            pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 3)

    def draw_hand(self, length, angle, color, width):
        end_x = self.center[0] + length * np.cos(np.radians(angle))
        end_y = self.center[1] + length * np.sin(np.radians(angle))
        pygame.draw.line(self.screen, color, self.center, (end_x, end_y), width)

    def calculate_hand_angles(self, hours, minutes):
        # Convert 24-hour format to 12-hour format for analog clock
        #  - 90 is the move the angle from 0 degree to start at "12" and not at "9" as start marker
        #  each hour is 30 degree.
        #  we also calculate the addition of the minutes to the hours pointer
        hour_angle = (hours % 12 + minutes / 60) * 30 - 90
        #  360 / 60 = 6 so we multiplty by 6 to compensate
        minute_angle = minutes * 6 - 90
        return hour_angle, minute_angle

    def run_display_loop(self, hours, minutes):
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            # drawing the clock circle with markers for hours
            self.draw_clock_face()

            # calculating the angles of the pointers
            hour_angle, minute_angle = self.calculate_hand_angles(hours, minutes)

            # drawing the pointers for hours and minutes
            self.draw_hand(80, hour_angle, (0, 0, 0), 6)
            self.draw_hand(120, minute_angle, (0, 0, 0), 4)

            self.exitButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exitButton.check_clicked(event):
                        running = False
            # update the drawing
            pygame.display.flip()
            # set to update per second
            self.clock.tick(1)

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
    return time_input_as_int[0], time_input_as_int[1]


def draw_clock_based_on_digital_time_input(time_input):

    clock = ClockDisplay(1000, 600)
    hours, minutes = parse_string_time_input(time_input)
    clock.run_display_loop(hours, minutes)


def generate_clock_image(time):
    clock = ClockDisplay(1000, 600)
    try:
        hours, minutes = parse_string_time_input(time)
    except Exception:
        print("error with time received, generate time using random input")
        hours = randint(0,11)
        minutes = randint(0,59)
    return clock.generate_clock_image(hours, minutes)



def find_circle_center(image):
    global debug
    #  needed to blurr twice for accurate result. need to understand why
    img = cv2.medianBlur(image, 5)
    img = cv2.medianBlur(img, 3)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 200,
                              param1=70, param2=20, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.round(circles[0, :]))
        # Assuming the largest circle detected is the clock face
        x, y, r = circles[0]
        return (x, y), r
    else:
        raise ValueError("No clock face found.")
    # circles = np.uint16(np.around(circles))
    # for i in circles[0, :]:
    #     # if debug:
    #     #     # draw the outer circle
    #     #     cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #     #     # draw the center of the circle
    #     #     cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    #     #     cv2.imshow('detected circles', cimg)
    #     #     cv2.waitKey(0)
    #     #     cv2.destroyAllWindows()
    #     return i[0], i[1]. i[2]
    #
    # # if we got here we failed to find the circle.
    # raise Exception("didnt find circle")


# in this function we take the image, blur it and look for lines using HoughLines
# based on logic found in opencv's site and https://stackoverflow.com/questions/54188478/opencv-houghlines-not-detecting-lines
def find_minutes_time(image):
    global debug
    # Apply Canny edge detection
    # i dont know why blurring twice worked. need to research that
    # image = cv2.medianBlur(image, 5)
    # edges = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), 50, 150, apertureSize=3)
    edges = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), 50, 150)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=80)
    # lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=90, minLineLength=30, maxLineGap=5)

    # Draw the lines on the original image
    if lines is not None:
        for line in lines:
            # x1, y1, x2, y2 = line[0]
            # Convert polar coordinates to Cartesian coordinates
            theta, rho = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
            if debug:
                cv2.imshow("Lines Detected", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return x0, y0, image
    return -1, -1, image

# same logic as the function above but for hours.
# there is code duplication here. need to combine to 1 function to save logic.
def find_hours_time(image):
    global debug
    # Apply Canny edge detection
    image = cv2.medianBlur(image, 5)
    image = cv2.medianBlur(image, 3)

    edges = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=60)

    # Draw the lines on the original image
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            # Convert polar coordinates to Cartesian coordinates
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            return x0, y0
    if debug:
        cv2.imshow("Lines Detected", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return -1, -1

def find_lines(image):
    global debug
    edges = cv2.Canny(image, 50, 150)

    # Use the Hough method to find straight lines from the edges
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=70, minLineLength=10, maxLineGap=10)
    # if debug:
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(image, (x1, y1), (x2, y2), (50, 50, 0), 2)
    #         cv2.imshow("Lines Detected", image)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()
    return lines

def calculate_angle(center, line):
    x1, y1, x2, y2 = line
    # dx, dy = line[0] - center[0], center[1] - line[1]
    dx, dy = x2 - center[0], y2 - center[1]
    up = (0, -1)
    dot = np.dot(up, (dx, dy))
    # dot = np.dot(center, (dx, dy))

    # the direction of the center vector is "12"

    cos_angle = dot / (np.linalg.norm((dx, dy)))
    # return np.degrees(np.acos(dot / (np.linalg.norm((dx, dy)) * np.linalg.norm((0, 100)))))

    angle = np.degrees(np.acos(cos_angle))
    #
    if dx < 0:
        angle = 360 - angle
    return angle
    # return angle if angle >= 0 else angle + 360


def find_hand_angles(hour_line, minute_line, center):
    # for line in lines:
    #     line = line.squeeze()
    #     x1, y1, x2, y2 = line
    #
    #     length = np.hypot(x2 - x1, y2 - y1)
    #     if length > max_length:
    #         # Longer line is more likely to be the minute hand
    #         if minute_hand is not None:
    #             hour_hand = minute_hand  # Reassign the previous longest as hour hand
    #         minute_hand = line
    #         max_length = length
    #     elif hour_hand is None or length < max_length * 0.9:
    #         hour_hand = line
    #         # Calculate angles for hour and minute hands
    # if hour_hand is not None and minute_hand is not None:

    hour_angle = calculate_angle(center, hour_line)
    minute_angle = calculate_angle(center, minute_line)
        # angle1 = calculate_angle(center, (x1, y1))
        # angle2 = calculate_angle(center, (x2, y2))
        #
        # # Use the longer line as the minute hand, shorter as hour hand
        # if length > max_length:
        #     minute_hand = angle1 if length == max_length else max(angle1, angle2)
        #     hour_hand = angle1 if length < max_length else min(angle1, angle2)
        #     max_length = length

    return hour_angle, minute_angle

def line_starts_near_center(line, center, tolerance=10):
    x1, y1, x2, y2 = line
    centerx, centery = center
    # Check if either endpoint is within the tolerance around the center
    if abs(x1 - centerx) <= centerx / tolerance and abs(y1 - centery) <= centery / tolerance:
        # (x1, y1) is already near the center; no need to move
        return True
        # return (x1, y1, x2, y2)
    elif abs(x2 - centerx) <= centerx / tolerance and abs(y2 - centery) <= centery / tolerance:
        # (x2, y2) is already near the center; no need to move
        return True
    return False
    # else:
    #     # Calculate the shift to move (x1, y1) to (centerx, centery)
    #     dx = centerx - x1
    #     dy = centery - y1
    #
    #     # Move both endpoints by the same shift
    #     line[0] = x1 + dx
    #     line[1] = y1 + dy
    #     line[2] = x2 + dx
    #     line[3] = y2 + dy
    #
    #     return line

def organize_lines(lines, center):
    max_length = 0
    minute_hand = None
    hour_hand = None

    for line in lines:
        line = line.squeeze()
        if not line_starts_near_center(line,center):
            continue
        x1, y1, x2, y2 = line

        if abs(y1 - center[1]) > center[1] * 0.1:
            line[0] = x2
            line[1] = y2
            line[2] = x1
            line[3] = y1
        # if abs(x1 - center[0]) > center[0] * 0.1:
        #     line[2] = x1
        #     line[0] = center[0]

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

# main function. checks that the image we received
def translate_to_digital(file):
    if not exists(file):
        print(f"The file provided {file} does not exist")
        exit()
    # image = cv2.imread(file, cv2.)
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    try:
        center, radius = find_circle_center(image)
    except Exception as e:
        print(f"failed to find the clock's circle. {e}")
        exit()

    lines = find_lines(image)

    hour_line , minutes_line = organize_lines(lines, center)
    color_layer = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if hour_line is None:
        hour_line = minutes_line
    cv2.line(color_layer, (hour_line[0], hour_line[1]), (hour_line[2], hour_line[3]), (255, 0, 0), 2)
    cv2.line(color_layer, (minutes_line[0], minutes_line[1]), (minutes_line[2], minutes_line[3]), (0, 0, 255), 2)

    cv2.imshow("Lines Detedasdasdascted", color_layer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    hours, minutes = find_hand_angles(hour_line, minutes_line, center)
    print(lines)
    # x0_seconds, y0_seconds, image = find_minutes_time(image)
    # if x0_seconds == -1 or y0_seconds == -1:
    #     print("error in getting the minutes indication")
    #     exit()
    #
    # x0_hours, y0_hours = find_hours_time(image)
    # if x0_hours == -1 or y0_hours == -1:
    #     print("error in getting the hours indication")
    #     exit()
    # # function to turn the given dx dy to the correct angle and than transform it to the digital tim representation
    # minutes = ((np.degrees(np.atan2(y0_seconds-center_y, x0_seconds-center_x)) + 90) % 360) // 6 # each 6 degrees is 1 minute
    # hours = ((np.degrees(np.atan2(y0_hours-center_y, x0_hours-center_x)) + 90) % 360) // 30# each 6 degrees is 1 minute

    #  allow a 10% diviation when calculating the angle. so for example the angle 59 degrees will cound as 2 and not as 1
    if hours // 30 < (hours + 3) // 30:
        hours += 3
    hours = hours // 30
    minutes = minutes // 6
    print(F"the time is {int(hours)}:{int(minutes)}")


def main():
    global debug
    parser = argparse.ArgumentParser(description="Draw a clock at a specified time.")
    parser.add_argument("--draw_time", action='store_true', required=False, help="draw the clock.")
    parser.add_argument("--time", type=str, required=False, help="Time in the format 'HH:MM' ")
    parser.add_argument("--create_clock_images", action='store_true', required=False, help="create an image of a clock")
    parser.add_argument("--translate_to_digital", type=str, required=False, help="picture of a clock to translate to digital")
    parser.add_argument("--debug", action='store_true', required=False, help="debug mode to have prints mid-way")

    # Parse arguments
    args = parser.parse_args()
    if args.debug:
        debug = True
    if args.draw_time and args.time:
        draw_clock_based_on_digital_time_input(args.time)
    if args.create_clock_images:
        filename = generate_clock_image(args.time)
        translate_to_digital(filename)
    if args.translate_to_digital:
        translate_to_digital(args.translate_to_digital)


if __name__ == "__main__":
    main()
