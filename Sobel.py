# Re-import the necessary libraries
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the new image
input_image_path_pipes = '/mnt/data/Pipes_UV.1001.texture_test.png'
image_pipes = Image.open(input_image_path_pipes)
image_np_pipes = np.array(image_pipes)

# Convert to grayscale
gray_image_pipes = cv2.cvtColor(image_np_pipes, cv2.COLOR_RGBA2GRAY)

# Generate Normal Map using Sobel filter
sobelx_pipes = cv2.Sobel(gray_image_pipes, cv2.CV_32F, 1, 0, ksize=5)
sobely_pipes = cv2.Sobel(gray_image_pipes, cv2.CV_32F, 0, 1, ksize=5)

# Normalize Sobel results to get x and y gradients
sobelx_pipes = sobelx_pipes / np.max(np.abs(sobelx_pipes)) * 0.5 + 0.5
sobely_pipes = sobely_pipes / np.max(np.abs(sobely_pipes)) * 0.5 + 0.5

# Create Normal Map with x, y gradients and constant z component
normal_map_pipes = np.zeros((gray_image_pipes.shape[0], gray_image_pipes.shape[1], 3), dtype=np.float32)
normal_map_pipes[:, :, 0] = sobelx_pipes  # Red channel for x
normal_map_pipes[:, :, 1] = sobely_pipes  # Green channel for y
normal_map_pipes[:, :, 2] = 1.0           # Blue channel for z

# Normalize to 0-255 and convert to uint8
normal_map_pipes = (normal_map_pipes * 255).astype(np.uint8)

# Generate Bump Map using grayscale with histogram equalization
bump_map_pipes = cv2.equalizeHist(gray_image_pipes)

# Save the normal map and bump map
normal_map_output_path_pipes = '/mnt/data/Pipes_UV_Texture_Normal_Map.png'
bump_map_output_path_pipes = '/mnt/data/Pipes_UV_Texture_Bump_Map.png'
Image.fromarray(normal_map_pipes).save(normal_map_output_path_pipes)
Image.fromarray(bump_map_pipes).save(bump_map_output_path_pipes)

# Display the results
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(image_np_pipes)

plt.subplot(1, 3, 2)
plt.title("Normal Map")
plt.imshow(normal_map_pipes)

plt.subplot(1, 3, 3)
plt.title("Bump Map")
plt.imshow(bump_map_pipes, cmap='gray')

plt.show()
