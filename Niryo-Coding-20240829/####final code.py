####final code

import cv2
import numpy as np
import pyniryo
from pyniryo2 import Vision, NiryoRos

# Define the positions for the Tic Tac Toe field and turn indicators
positions = {
    "p1": (257, 146),
    "p2": (327, 139),
    "p3": (400, 139),
    "p4": (255, 209),
    "p5": (330, 206),
    "p6": (402, 206),
    "p7": (255, 280),
    "p8": (330, 280),
    "p9": (405, 279)
}

indications = {
    "I1": (472, 151),  # Indication point for player 1
    "I2": (480, 258)   # Indication point for player 2
}

# HSV color ranges for red, green, and blue
color_ranges = {
    'red': ([160, 100, 100], [180, 255, 255]),  # Lower and upper bounds for red
    'green': ([40, 50, 50], [80, 255, 255]),    # Lower and upper bounds for green
    'blue': ([100, 150, 0], [140, 255, 255])    # Lower and upper bounds for blue
}

# Colors for drawing rectangles
draw_colors = {
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0)
}

# Initialize the Niryo robot's ROS instance and vision system
ros_instance = NiryoRos("169.254.200.200")
vision = Vision(ros_instance)

# Function to detect color in a given position
def detect_color(hsv_frame, pos, region_size=10):
    x, y = pos
    # Define the region of interest (ROI) around the pixel
    x_start = max(0, x - region_size)
    y_start = max(0, y - region_size)
    x_end = min(hsv_frame.shape[1], x + region_size)
    y_end = min(hsv_frame.shape[0], y + region_size)
    
    region = hsv_frame[y_start:y_end, x_start:x_end]
    
    # Calculate the mean color of the region
    mean_color = cv2.mean(region)[:3]  # Get the average color in the region (ignore alpha channel)
    mean_color = np.array(mean_color, dtype=np.uint8)

    # Check if the mean color falls within any predefined color ranges
    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)

        # Check if the mean color is within the color range
        if all(lower_bound <= mean_color) and all(mean_color <= upper_bound):
            return color_name  # Return the detected color
    return "none"  # Return 'none' if no color matches

# Initialize a state dictionary to store current colors of each position
state = {pos_name: "none" for pos_name in positions.keys()}

# Variable to track if the latest state has already been printed
last_printed_blue_positions = []

# Function to continuously monitor and return the blue chip positions when I2 is red
def continuously_monitor_game():
    global last_printed_blue_positions  # Reference the global variable for comparison
    
    while True:
        # Capture the image from the Niryo robot camera
        img_compressed = vision.get_img_compressed()
        img_uncompressed = pyniryo.uncompress_image(img_compressed)
        camera_info = vision.get_camera_intrinsics()
        img = pyniryo.undistort_image(img_uncompressed, camera_info.intrinsics, camera_info.distortion)

        # Resize the frame for display and processing
        frame = cv2.resize(img, (640, 480))

        # Convert the image to HSV for better color detection
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Check if 'I2' is red
        i2_color = detect_color(hsv_frame, indications["I2"])
        if i2_color == "red":
            # Update state and capture the game state (only blue positions)
            current_blue_positions = []
            for pos_name, pos in positions.items():
                detected_color = detect_color(hsv_frame, pos)
                if detected_color != state[pos_name]:  # If the color has changed
                    state[pos_name] = detected_color

                if detected_color == "blue":  # Only track positions with blue
                    current_blue_positions.append(pos_name)

            # Check if the current state of blue positions is different from the last one printed
            if current_blue_positions != last_printed_blue_positions:
                print(f"Positions with blue: {current_blue_positions}")
                last_printed_blue_positions = current_blue_positions.copy()

        # Check if 'q' key has been pressed to break the loop (optional for manual break)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources
    cv2.destroyAllWindows()

# Start monitoring
continuously_monitor_game()
