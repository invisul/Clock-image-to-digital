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

Usage Example: python ClockDigitalAnalogTransformation.py --draw_time "14:30"
This will generate an analog clock showing 2:30 PM.

Here is an example of draw_time usage and result 
![image](https://github.com/user-attachments/assets/b91eb209-1393-405c-a625-8d28327d202e)

![image](https://github.com/user-attachments/assets/0d0c26e0-82ce-4c4c-86cf-2df598a31240)



2. --create_clock_images
Description: Creates a specified number of images with random times displayed on analog clocks.

Input: The number of images to create.

File Naming:
Each generated image is saved with a filename pattern: clock_{current_time}.png, where {current_time} is the timestamp of image creation.
Usage Example: python ClockDigitalAnalogTransformation.py --create_clock_images 5
This will generate 5 clock images with random times.

Here is an example of a clock image generated using 
![image](https://github.com/user-attachments/assets/e5c9ed1b-35f3-4cf5-911c-cd679ba19b37)

![clock_1730744361 855784](https://github.com/user-attachments/assets/5ffac6f2-1347-46a8-8cdd-fe8037d8b372)



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
Usage Example: python ClockDigitalAnalogTransformation.py --translate_to_digital path/to/clock_image.png


Picture example of translate_to_digital
![image](https://github.com/user-attachments/assets/6e2bf4e5-367d-4231-b88f-bb7126526d56)



4. --debug
Description: Activates debug mode to show intermediary results during processing.
Functionality:
This option displays updates as each step completes:
After the circle (clock face) is detected, it changes color.
After the minute hand is found, it is removed from the image.
After the hour hand is found, a black line is drawn over it.
Usage Example:
python ClockDigitalAnalogTransformation.py --translate_to_digital path/to/clock_image.png --debug

This will show intermediary steps as the analog time is converted to digital.



