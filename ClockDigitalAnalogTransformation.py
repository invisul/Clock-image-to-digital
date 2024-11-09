import cv2
from os.path import exists, join
from os import getcwd, remove, rmdir
from ClockDisplay import ClockDisplay
import argparse
from random import randint
from util import parse_string_time_input, find_circle_center, find_lines, find_hand_angles, organize_lines


# The function receives time in the format "HH:MM" and draws the clock using pygame
def draw_clock_based_on_digital_time_input(time_input):
    clock = ClockDisplay(1000, 600)
    hours, minutes = parse_string_time_input(time_input)
    clock.run_display_loop(hours, minutes)


# Function generates a png image of given time.
# time = time in "HH:MM" format
# output = path to where to save the image. if not provided. will use the running directory and the name
#  clock_{timestamp}.png timestamp representing the time of creation
def generate_clock_image(time, output):
    clock = ClockDisplay(1000, 600)
    try:
        hours, minutes = parse_string_time_input(time)
    except Exception:
        print("error with time received, generate time using random input")
        hours = randint(0,11)
        minutes = randint(0,59)
    return clock.generate_clock_image(hours, minutes, output)


# Function receive a image file containing a clock and returns the digital value of the clock in the image
# debug - if debug is provided, will print the results of openCV algorithms to show the circle/ lines found
def translate_to_digital(file, debug):
    if not exists(file):
        print(f"The file provided {file} does not exist")
        exit()
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    try:
        center, radius = find_circle_center(image, debug)
    except Exception as e:
        print(f"failed to find the clock's circle. {e}")
        exit()

    lines = find_lines(image, debug)

    hour_line, minutes_line = organize_lines(lines, center)
    if hour_line is None and minutes_line is None:
        print("failed to find clock lines for some reason, exiting")
        exit()
    if hour_line is None:
        hour_line = minutes_line

    if debug:
        color_layer = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.line(color_layer, (hour_line[0], hour_line[1]), (hour_line[2], hour_line[3]), (255, 0, 0), 2)
        cv2.line(color_layer, (minutes_line[0], minutes_line[1]), (minutes_line[2], minutes_line[3]), (0, 0, 255), 2)

        cv2.imshow("Lines found Red=Minutes", color_layer)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    hours, minutes = find_hand_angles(hour_line, minutes_line, center)

    #  allow a 10% diviation when calculating the angle. so for example the angle 59 degrees will cound as 2 and not as 1
    if hours // 30 < (hours + 3) // 30:
        hours += 3
    hours = (hours // 30) % 12
    minutes = minutes // 6
    print(F"the time is {int(hours)}:{int(minutes)}")
    return hours, minutes


# Unit test inner function
def run_unit_test(unit_testing_directory, filename, time_value, debug):
    hours, minutes = parse_string_time_input(time_value)
    test_output = join(unit_testing_directory, filename)
    created_file = generate_clock_image(time_value, test_output)
    hours_res, minutes_res = translate_to_digital(created_file, debug)
    if not debug:
        remove(test_output)
    if hours != hours_res or minutes + 1 < minutes_res and minutes_res < minutes - 1:
        return False
    return True


# unit testing function to run multiple tests
def unit_test(debug):
    passed_tests = []
    failed_tests = []
    unit_testing_directory = join(getcwd(), "unit_test")
    straight_line_test = {"test_name": "straight_line_test",
                          "file_name": "straight_line_test.png",
                          "time_value": "01:37"}
    overlaaping_test = {"test_name": "overlap_test",
                          "file_name": "overlap_test.png",
                          "time_value": "01:05"}
    edge_case1_test = {"test_name": "edge_case1_test",
                        "file_name": "case1_test.png",
                        "time_value": "11:59"}
    edge_case2_test = {"test_name": "edge_case2_test",
                  "file_name": "case2_test.png",
                  "time_value": "00:00"}
    case3_test = {"test_name": "case3_test",
                  "file_name": "case3_test.png",
                  "time_value": "02:35"}
    case4_test = {"test_name": "case4_test",
                  "file_name": "case4_test.png",
                  "time_value": "17:27"}
    case5_test = {"test_name": "case5_test",
                  "file_name": "case5_test.png",
                  "time_value": "7:14"}
    all_tests = [straight_line_test, overlaaping_test, edge_case1_test, edge_case2_test, case3_test, case4_test, case5_test]
    for test in all_tests:
        test_name = test["test_name"]
        if run_unit_test(unit_testing_directory, test["file_name"], test["time_value"], debug):
            print(f"passed test {test_name}")
            passed_tests.append(test_name)
        else:
            print(f"failed test {test_name}")
            failed_tests.append(test_name)

    print(f"passed a total of {len(passed_tests)} tests")
    print(f"failed a total of {len(failed_tests)} tests")
    if not debug:
        rmdir(unit_testing_directory)


def main():
    parser = argparse.ArgumentParser(description="Draw a clock at a specified time.")
    parser.add_argument("--draw_time", action='store_true', required=False, help="draw the clock.")
    parser.add_argument("--time", type=str, required=False, help="Time in the format 'HH:MM' ")
    parser.add_argument("--create_clock_images", action='store_true', required=False, help="create an image of a clock")
    parser.add_argument("--translate_to_digital", type=str, required=False, help="picture of a clock to translate to digital")
    parser.add_argument("--debug", action='store_true', required=False, help="debug mode to have prints mid-way")
    parser.add_argument("-o", "--output", type=str, help="Output directory to clock image")
    parser.add_argument("-ut", "--unit_test", action='store_true', help="Unit testing")

    # Parse arguments
    args = parser.parse_args()
    if args.unit_test:
        unit_test(args.debug)
    if args.draw_time and args.time:
        draw_clock_based_on_digital_time_input(args.time)
    if args.create_clock_images:
        filename = generate_clock_image(args.time, args.output)
        translate_to_digital(filename)
    if args.translate_to_digital:
        translate_to_digital(args.translate_to_digital, args.debug)


if __name__ == "__main__":
    main()
