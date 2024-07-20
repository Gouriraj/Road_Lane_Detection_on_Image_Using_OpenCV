# -*- coding: utf-8 -*-
"""RoadLaneDetection_for _image.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17I9x-XRaMtjlhTv41AuQDdNOa6D6eEXW
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

def region_of_interest(image, vertices):
    # Create a mask that is the same size as the image, but filled with zeros (black)
    mask = np.zeros_like(image)
    match_mask_color = 255  # The color used to fill the mask (white)

    # Fill the polygon defined by vertices with the match_mask_color
    cv2.fillPoly(mask, vertices, match_mask_color)

    # Perform a bitwise AND operation to keep only the region defined by the mask
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def draw_lines(img, lines):
    # Make a copy of the original image
    img = np.copy(img)

    # Create a blank image with the same dimensions as the original image
    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    # Iterate over the lines and draw them on the blank image
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=4)

    # Combine the original image with the lines using weighted sum
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

# Read the image from a file
image = cv2.imread('road3.jpg')
# Convert the image from BGR to RGB color space
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print(image.shape)  # Print the shape of the image (height, width, channels)
height = image.shape[0]
width = image.shape[1]
print(height, width)  # Print the height and width of the image

# Define the vertices of the region of interest (a triangle in this case)
vertices = [
    (0, height),
    (width / 2, height / 2),
    (width, height)
]

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# Apply the Canny edge detector to the grayscale image
canny_image = cv2.Canny(gray_image, 125, 175)

# Apply the region_of_interest function to the edge-detected image
new_image = region_of_interest(canny_image, np.array([vertices], np.int32))

# Detect lines in the masked edge-detected image using Hough Transform
lines = cv2.HoughLinesP(new_image,
                        rho=2,
                        theta=np.pi/180,
                        threshold=160,
                        lines=np.array([]),
                        minLineLength=40,
                        maxLineGap=25)

# Draw the detected lines on the original image
image_with_lines = draw_lines(image, lines)

print("ORIGINAL IMAGE:")
# Display the original image using matplotlib
plt.imshow(image)
plt.show()

print("DETECTED IMAGE:")
# Display the image with lines using matplotlib
plt.imshow(image_with_lines)
plt.show()

"""# New Section"""

from google.colab import drive
drive.mount('/content/drive')