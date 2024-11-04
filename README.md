Clock Image Generator and Analyzer - README
This tool provides various functionalities for generating analog clock images, drawing specific times, and translating analog clock images to digital time. Below are explanations for each command-line argument:

This code require OpenCV and pygame to run, please run the makefile provided or install the packages yourself

Arguments
1. --draw_time
Description: Draws an analog clock with the specified time.
Input Format: "HH:MM" (24-hour format).
Logic:
Each hour corresponds to 30 degrees on the clock (since a full 360 degrees are divided by 12 hours).
Each minute corresponds to 6 degrees (since 360 degrees divided by 60 minutes equals 6).
Usage Example: python clock_tool.py --draw_time "14:30"
This will generate an analog clock showing 2:30 PM.


2. --create_clock_images
Description: Creates a specified number of images with random times displayed on analog clocks.
Input: The number of images to create.
File Naming:
Each generated image is saved with a filename pattern: clock_{current_time}.png, where {current_time} is the timestamp of image creation.
Usage Example: python clock_tool.py --create_clock_images 5
This will generate 5 clock images with random times.


3. --translate_to_digital
Description: Reads an analog clock image, identifies the hour and minute hands, and translates it to digital time.
Input: Path to the analog clock image.
Logic:
Find the Circle: Identify the clock face (circle) and locate its center.
Identify the Minute Hand:
Detect the minute hand by analyzing angles relative to the center, using atan2 to calculate the angle.
Remove the Minute Hand: Remove the minute hand from the image to simplify detecting the hour hand.
Identify the Hour Hand:
Detect the hour hand by repeating the angle analysis process.
Once both hands are identified, calculate the time based on their angles.
Usage Example: python clock_tool.py --translate_to_digital path/to/clock_image.png


4. --debug
Description: Activates debug mode to show intermediary results during processing.
Functionality:
This option displays updates as each step completes:
After the circle (clock face) is detected, it changes color.
After the minute hand is found, it is removed from the image.
After the hour hand is found, a black line is drawn over it.
Usage Example:
python clock_tool.py --translate_to_digital path/to/clock_image.png --debug

This will show intermediary steps as the analog time is converted to digital.
