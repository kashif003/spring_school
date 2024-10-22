import cv2
import numpy as np
import pyniryo
from pyniryo2 import Vision, NiryoRos

# Define the positions for the Tic Tac Toe field and turn indicators
positions = {
    "p1": (276, 152),
    "p2": (347, 149),
    "p3": (426, 145),
    "p4": (279, 223),
    "p5": (358, 214),
    "p6": (424, 215),
    "p7": (278, 296),
    "p8": (355, 291),
    "p9": (435, 288)
}

indications = {
    "I1": (201, 171),  # Indication point for player 1
    "I2": (207, 278)   # Indication point for player 2
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
import time

def detect_color(hsv_frame, pos, region_size=10):
    x, y = pos
    x_start = max(0, x - region_size)
    y_start = max(0, y - region_size)
    x_end = min(hsv_frame.shape[1], x + region_size)
    y_end = min(hsv_frame.shape[0], y + region_size)
    
    region = hsv_frame[y_start:y_end, x_start:x_end]
    
    mean_color = cv2.mean(region)[:3]
    mean_color = np.array(mean_color, dtype=np.uint8)

    for color_name, (lower, upper) in color_ranges.items():
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)

        if all(lower_bound <= mean_color) and all(mean_color <= upper_bound):
            return color_name
    return "none"


state = {pos_name: "none" for pos_name in positions.keys()}
last_printed_green_positions = []

def positions_played():
    global last_printed_green_positions
    
    while True:
        img_compressed = vision.get_img_compressed()
        img_uncompressed = pyniryo.uncompress_image(img_compressed)
        camera_info = vision.get_camera_intrinsics()
        img = pyniryo.undistort_image(img_uncompressed, camera_info.intrinsics, camera_info.distortion)
        frame = cv2.resize(img, (640, 480))
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        i2_color = detect_color(hsv_frame, indications["I2"])
        if i2_color == "red":
            current_green_positions = []
            time.sleep(3)
            for pos_name, pos in positions.items():
                detected_color = detect_color(hsv_frame, pos)
                if detected_color != state[pos_name]:
                    state[pos_name] = detected_color

                if detected_color == "green":
                    current_green_positions.append(pos_name)

            if current_green_positions != last_printed_green_positions:
                print(f"Positions with green: {current_green_positions}")

                new_position = list(set(current_green_positions)-set(last_printed_green_positions))
                last_printed_green_positions = current_green_positions.copy()
                
                if not  len(new_position)<1:
                   return new_position

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
