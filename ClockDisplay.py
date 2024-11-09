import pygame
import time
import math
import sys
import cv2
from os.path import exists, dirname, join
from os import makedirs, getcwd, remove, rmdir
import numpy as np
import argparse
from random import randint

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

    def generate_clock_image(self, hours, minutes, filename=None):
        # drawing the clock circle with markers for hours
        # creating a white screen
        self.screen.fill((255, 255, 255))
        # Generate a unique filename with the current date and time
        timestamp = time.time()
        if filename and not exists(filename):
            directory_name = dirname(filename)
            if directory_name == "":
                filename = join(getcwd(), filename)
            makedirs(directory_name, exist_ok=True)
        if filename is None:
            filename = f"clock_{timestamp}.png"
            print(f"no file name is provided, using current directory as the path and name of the file will be {filename}")
        # drawing the clock itself (the circle)
        self.draw_clock_face()

        # calculating the angles of the pointers
        hour_angle, minute_angle = self.calculate_hand_angles(hours, minutes)

        # drawing the pointers for hours and minutes
        self.draw_hand(80, hour_angle, (0, 0, 0), 8)
        self.draw_hand(120, minute_angle, (0, 0, 0), 6)

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