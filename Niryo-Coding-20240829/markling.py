

import cv2
import torch
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

# Load pre-trained SAM model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


import requests

url = 'https://path/to/sam_vit_h.pth'  # Replace with actual URL to the checkpoint file
local_filename = 'sam_vit_h.pth'




with requests.get(url, stream=True) as r:
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

sam_checkpoint = "sam_vit_h.pth"

model_type = "vit_h"  # Options: 'vit_h', 'vit_l', 'vit_b'

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device)

# SAM predictor
predictor = SamPredictor(sam)

# Initialize video capture (0 for webcam)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Resize the frame for faster processing (optional)
    original_frame = frame.copy()
    height, width, _ = frame.shape
    input_image = cv2.resize(frame, (512, 512))  # Resize for faster inference

    # Convert to the format SAM expects (normalized, RGB image)
    input_image_rgb = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

    # Set the image for the predictor
    predictor.set_image(input_image_rgb)

    # Optionally, provide a prompt (point, box, etc.). Here we use auto-masking
    masks, _, _ = predictor.predict(auto_mask=True)  # For auto-segmentation

    # Resize mask back to original frame size
    mask_resized = cv2.resize(masks[0], (width, height))

    # Convert mask to 3-channel image and overlay on original frame
    mask_overlay = (mask_resized * 255).astype(np.uint8)
    mask_overlay = cv2.cvtColor(mask_overlay, cv2.COLOR_GRAY2BGR)

    # Blend the mask with the original frame
    blended = cv2.addWeighted(original_frame, 0.6, mask_overlay, 0.4, 0)

    # Show the segmented output
    cv2.imshow('Segment Anything - Real-time', blended)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break