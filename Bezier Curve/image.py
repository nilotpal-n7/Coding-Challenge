import cv2
import numpy as np

# Load the image
image_path = 'drawing.png'  # Replace with your image path
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to detect black regions
_, black_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

# Find contours of the black regions
contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Create a list to store boundary points
boundary_points = []

# Iterate through each contour
for contour in contours:
    for point in contour:
        x, y = point[0]  # Extract x and y coordinates
        boundary_points.append([x, y, 0])  # z = 0

# Convert the list to a NumPy array
boundary_array = np.array(boundary_points)

# Save the array to a .npy file
output_file = 'black_boundary_points.npy'
np.save(output_file, boundary_array)

print(f"Boundary points saved to {output_file}")

# Load the saved array
loaded_array = np.load(output_file)
print("Loaded boundary points:")
print(loaded_array)
