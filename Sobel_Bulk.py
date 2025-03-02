import os
import uuid
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import threading
import time

# Define input and output directories
input_directory = './import/'
output_directory = './export/'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all files in the input directory
file_list = os.listdir(input_directory)

def process_image(file_name):
    try:
        # Check if the file is an image
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Create a folder for the image in the output directory
            image_folder = os.path.join(output_directory, os.path.splitext(file_name)[0])
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            # Load the image
            input_image_path = os.path.join(input_directory, file_name)
            image = Image.open(input_image_path)
            image_np = np.array(image)

            # Save the imported image in the image folder
            imported_image_output_path = os.path.join(image_folder, f'{os.path.splitext(file_name)[0]}_imported.png')
            image.save(imported_image_output_path)

            # Convert to grayscale
            gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGBA2GRAY)

            # Generate Normal Map using Sobel filter
            sobelx = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=5)
            sobely = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=5)

            # Normalize Sobel results to get x and y gradients
            sobelx = sobelx / np.max(np.abs(sobelx)) * 0.5 + 0.5
            sobely = sobely / np.max(np.abs(sobely)) * 0.5 + 0.5

            # Create Normal Map with x, y gradients and constant z component
            normal_map = np.zeros((gray_image.shape[0], gray_image.shape[1], 3), dtype=np.float32)
            normal_map[:, :, 0] = sobelx  # Red channel for x
            normal_map[:, :, 1] = sobely  # Green channel for y
            normal_map[:, :, 2] = 1.0     # Blue channel for z

            # Normalize to 0-255 and convert to uint8
            normal_map = (normal_map * 255).astype(np.uint8)

            # Generate Bump Map using grayscale with histogram equalization
            bump_map = cv2.equalizeHist(gray_image)

            # Generate unique file names for normal map and bump map
            normal_map_output_path = os.path.join(image_folder, f'{os.path.splitext(file_name)[0]}_normal_map_{uuid.uuid4()}.png')
            bump_map_output_path = os.path.join(image_folder, f'{os.path.splitext(file_name)[0]}_bump_map_{uuid.uuid4()}.png')

            # Save the normal map and bump map in the image folder
            Image.fromarray(normal_map).save(normal_map_output_path)
            Image.fromarray(bump_map).save(bump_map_output_path)

            # Remove the imported image from the input directory
            os.remove(input_image_path)

            print(f"Processed {input_image_path}")

    except Exception as e:
        print(f"Error processing {input_image_path}: {str(e)}")

# Run threading to process multiple images at the same time
threads = []
for file_name in file_list:
    thread = threading.Thread(target=process_image, args=(file_name,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("Processing completed.")

# Continuously watch the import directory for new images and process them as soon as they are added
while True:
    # Check for new files in the input directory
    new_file_list = set(os.listdir(input_directory)) - set(file_list)

    if new_file_list:
        print(f"New files detected: {new_file_list}")
        file_list.extend(new_file_list)

        # Process new files
        for file_name in new_file_list:
            thread = threading.Thread(target=process_image, args=(file_name,))
            thread.start()

    time.sleep(1)  # Adjust the sleep interval as needed
