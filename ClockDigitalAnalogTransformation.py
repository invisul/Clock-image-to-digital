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
        self.center = (width // 2 + randint(-50, 50), height//2 + randint(-50, 50))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)
        self.circle_size = randint(160, 250)

        button_font = pygame.font.Font(None, 24)
        button_color = pygame.Color('blue')
        button_text_color = pygame.Color('white')
        self.exitButton = Button(pygame.Rect(width // 3 - self.circle_size, 460, 100, 40), "Close",  button_font, button_color, button_text_color)

    def __del__(self):
        pygame.quit()

    def generate_random_clock_image(self, counter):
        # drawing the clock circle with markers for hours
        for i in range(counter):
            # creating a white screen
            self.screen.fill((255, 255, 255))
            # Generate a unique filename with the current date and time
            timestamp = time.time()
            filename = f"clock_{timestamp}.png"
            hours = randint(0, 24)
            minutes = randint(0, 59)

            # drawing the clock itself (the circle)
            self.draw_clock_face()

            # calculating the angles of the pointers
            hour_angle, minute_angle = self.calculate_hand_angles(hours, minutes)

            # drawing the pointers for hours and minutes
            self.draw_hand(80, hour_angle, (0, 0, 0), 6)
            self.draw_hand(120, minute_angle, (0, 0, 0), 4)

            # Save the current screen as a PNG image
            pygame.image.save(self.screen, filename)
            print(f"Clock image saved as {filename}")

    def draw_clock_face(self):
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.circle_size, 3)
        for hour in range(12):
            angle = math.radians(hour * 30)
            start_x = self.center[0] + (self.circle_size - 15) * math.cos(angle)
            start_y = self.center[1] + (self.circle_size - 15) * math.sin(angle)
            end_x = self.center[0] + self.circle_size * math.cos(angle)
            end_y = self.center[1] + self.circle_size * math.sin(angle)
            pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (end_x, end_y), 3)

    def draw_hand(self, length, angle, color, width):
        end_x = self.center[0] + length * math.cos(math.radians(angle))
        end_y = self.center[1] + length * math.sin(math.radians(angle))
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


def draw_clock_based_on_digital_time_input(time_input):
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
        clock = ClockDisplay(1000, 600)
        clock.run_display_loop(time_input_as_int[0], time_input_as_int[1])
    except ValueError:
        print(f"unknown error has occured while parsing {time_input}")


def generate_random_clock_image(num_to_create):
    if num_to_create < 0:
        print("number of images to generate cant be negative")
        exit()
    clock = ClockDisplay(1000, 600)
    clock.generate_random_clock_image(num_to_create)


def find_circle_center(image):
    global debug
    #  needed to blurr twice for accurate result. need to understand why
    img = cv2.medianBlur(image, 5)
    img = cv2.medianBlur(img, 3)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 200,
                              param1=70, param2=20, minRadius=0, maxRadius=0)

    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        if debug:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
            cv2.imshow('detected circles', cimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return i[0], i[1]

    # if we got here we failed to find the circle.
    raise Exception("didnt find circle")


# in this function we take the image, blur it and look for lines using HoughLines
# based on logic found in opencv's site and https://stackoverflow.com/questions/54188478/opencv-houghlines-not-detecting-lines
def find_minutes_time(image):
    global debug
    # Apply Canny edge detection
    # i dont know why blurring twice worked. need to research that
    image = cv2.medianBlur(image, 5)
    image = cv2.medianBlur(image, 3)
    edges = cv2.Canny(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLines(edges, rho=1, theta=np.pi / 180, threshold=100)

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
            cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
            if debug:
                cv2.imshow("Lines Detected", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            return x0, y0, image
    return -1, -1

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


# main function. checks that the image we received
def translate_to_digital(file):
    if not exists(file):
        print(f"The file provided {file} does not exist")
        exit()
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    try:
        center_x, center_y = find_circle_center(image)
    except Exception as e:
        print(f"failed to find the clock's circle. {e}")
        exit()
    x0_seconds, y0_seconds, image = find_minutes_time(image)
    if x0_seconds == -1 or y0_seconds == -1:
        print("error in getting the minutes indication")
        exit()

    x0_hours, y0_hours = find_hours_time(image)
    if x0_hours == -1 or y0_hours == -1:
        print("error in getting the hours indication")
        exit()
    # function to turn the given dx dy to the correct angle and than transform it to the digital tim representation
    minutes = ((math.degrees(math.atan2(y0_seconds-center_y, x0_seconds-center_x)) + 90) % 360) // 6 # each 6 degrees is 1 minute
    hours = ((math.degrees(math.atan2(y0_hours-center_y, x0_hours-center_x)) + 90) % 360) // 30# each 6 degrees is 1 minute
    print(F"the time is {int(hours)}:{int(minutes)}")


def main():
    global debug
    parser = argparse.ArgumentParser(description="Draw a clock at a specified time.")
    parser.add_argument("--draw_time", type=str, required=False, help="Time in the format 'HH:MM:SS' or 'HH:MM:SS'.")
    parser.add_argument("--create_clock_images", type=int, required=False, help="number of random clock images to generate")
    parser.add_argument("--translate_to_digital", type=str, required=False, help="picture of a clock to translate to digital")
    parser.add_argument("--debug", type=bool, required=False, help="debug mode to have prints mid-way")

    # Parse arguments
    args = parser.parse_args()
    if args.debug:
        debug = True
    if args.draw_time:
        draw_clock_based_on_digital_time_input(args.draw_time)
    if args.create_clock_images:
        generate_random_clock_image(args.create_clock_images)

    if args.translate_to_digital:
        translate_to_digital(args.translate_to_digital)


if __name__ == "__main__":
    main()
