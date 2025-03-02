import os
import uuid
import threading
import time
from tkinter import Tk, Text, Button, Label, END, DISABLED, NORMAL, Frame, PhotoImage, ttk
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Define input and output directories
input_directory = './import/'
output_directory = './export/'

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# List all files in the input directory
file_list = os.listdir(input_directory)

# Initialize variables
is_processing = False
total_images = len(file_list)
processed_images = 0

# Function to process images
def process_image(file_name):
    global is_processing, processed_images
    try:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Create a folder for the image in the output directory
            image_folder = os.path.join(output_directory, os.path.splitext(file_name)[0])
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)

            # Load the image
            input_image_path = os.path.join(input_directory, file_name)
            image = Image.open(input_image_path)
            image_np = np.array(image)

            # Get image details
            image_size = os.path.getsize(input_image_path)
            image_dimensions = image.size

            # Display image details in the log box
            log_text.insert(END, f"Processing {input_image_path}\n")
            log_text.insert(END, f"Size: {image_size} bytes\n")
            log_text.insert(END, f"Dimensions: {image_dimensions}\n")
            log_text.insert(END, "---------------------------------\n")
            log_text.see(END)

            # Rest of the image processing code...

            # Update the log box after processing each image
            log_text.insert(END, f"Processed {input_image_path}\n")
            log_text.see(END)

            # Update progress
            processed_images += 1
            status_label.config(text=f"Progress: {processed_images}/{total_images}")
            progress_bar["value"] = (processed_images / total_images) * 100
    except Exception as e:
        log_text.insert(END, f"Error processing {input_image_path}: {str(e)}\n")
        log_text.see(END)

# Function to start processing
def start_processing():
    global is_processing
    if not is_processing:
        is_processing = True
        button_start.config(state=DISABLED)
        button_pause.config(state=NORMAL)

        # Run threading to process multiple images at the same time
        threads = []
        for file_name in file_list:
            thread = threading.Thread(target=process_image, args=(file_name,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        is_processing = False
        button_start.config(state=NORMAL)
        button_pause.config(state=DISABLED)

# Function to pause processing
def pause_processing():
    global is_processing
    if is_processing:
        is_processing = False
        button_pause.config(state=DISABLED)
        button_start.config(state=NORMAL)

# Create the UI
root = Tk()
root.title("Image Processing")

# Main frame for better alignment
main_frame = Frame(root, padx=10, pady=10)
main_frame.grid(row=0, column=0)

# Logo frame
logo_frame = Frame(main_frame)
logo_frame.grid(row=0, column=0, pady=5)

# Logo image
logo_image = PhotoImage(file="logo.png")
logo_label = Label(logo_frame, image=logo_image)
logo_label.grid(row=0, column=0)

# Log box
log_text = Text(main_frame, height=10, width=50)
log_text.grid(row=1, column=0, padx=5, pady=5)

# Status label
status_label = Label(main_frame, text=f"Progress: 0/{total_images}")
status_label.grid(row=2, column=0, padx=5, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(main_frame, length=400, mode='determinate')
progress_bar.grid(row=3, column=0, padx=5, pady=5)

# Processing state label
processing_state_label = Label(main_frame, text="Waiting")
processing_state_label.grid(row=4, column=0, padx=5, pady=5)

# Start button
button_start = Button(main_frame, text="Start", command=start_processing)
button_start.grid(row=5, column=0, sticky='w', padx=5, pady=5)

# Pause button
button_pause = Button(main_frame, text="Pause", command=pause_processing, state=DISABLED)
button_pause.grid(row=5, column=0, sticky='e', padx=5, pady=5)

# Run the UI
root.mainloop()
