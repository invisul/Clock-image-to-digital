Needed Libararies are:
opencv-python
pygame
numpy

Clock Image Generator and Analyzer - README
This tool provides various functionalities for generating analog clock images, drawing specific times, and translating analog clock images to digital time. Below are explanations for each command-line argument:

This code require OpenCV and pygame to run, please run the makefile provided or install the packages yourself

Arguments
0. --time  Input Format: "HH:MM" (24-hour format).


1. --draw_time
Description: Draws an analog clock with the specified time.



Logic:
Each hour corresponds to 30 degrees on the clock (since a full 360 degrees are divided by 12 hours).
Each minute corresponds to 6 degrees (since 360 degrees divided by 60 minutes equals 6).

Usage Example: python ClockDigitalAnalogTransformation.py --draw_time --time "14:30"
This will generate an analog clock showing 2:30 PM.

Here is an example of draw_time usage and result 
<img width="1600" alt="image" src="https://github.com/user-attachments/assets/47d01032-3ff3-452e-ad60-60da92a285f3">




2. --create_clock_images
Description: Creates a specified number of images with random times displayed on analog clocks.

Input: The number of images to create.

File Naming:
Usage Example: python ClockDigitalAnalogTransformation.py --create_clock_images --time "12:30" --output "path_to_save.png"

or python ClockDigitalAnalogTransformation.py --create_clock_images will create a random image.
generated image is saved with a filename pattern:  clock_{current_time}.png, where {current_time} is the timestamp of image creation.

Here is an example of a clock image generated using 
<img width="1494" alt="image" src="https://github.com/user-attachments/assets/622cb8d9-8520-45bc-90de-fe2a6f4c3e31">
<img width="991" alt="image" src="https://github.com/user-attachments/assets/be1f199e-93e6-4935-9b39-6badc8f28d5a">




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


Examples of debug prints:

Circle found 
<img width="995" alt="image" src="https://github.com/user-attachments/assets/73af369e-0ee7-4c62-94f7-ce773ed3f66d">


Lines found using OpenCV algoirthm
<img width="810" alt="image" src="https://github.com/user-attachments/assets/7225222d-5f3b-4b65-ac7f-7f925b6468a6">


Clock Images from the internet example
<img width="786" alt="image" src="https://github.com/user-attachments/assets/f2686d2b-224d-42b5-b3e5-0799a65fa6aa">
<img width="604" alt="image" src="https://github.com/user-attachments/assets/e8db847e-d34e-4840-bd0a-bf24cb5ad783">

<img width="844" alt="image" src="https://github.com/user-attachments/assets/2d431362-0d04-4030-b10d-d770c9242269">


<img width="608" alt="image" src="https://github.com/user-attachments/assets/1c1c3645-7acc-463e-955e-f2c09e4387f3">




