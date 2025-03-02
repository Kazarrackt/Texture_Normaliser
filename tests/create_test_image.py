# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.4 - 2025-03-03
# ---

import os
import sys
import numpy as np
from PIL import Image, ImageDraw

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import logger from src directory
from src.logger import logger

# Create the import directory if it doesn't exist
import_dir = "./import/"
if not os.path.exists(import_dir):
    os.makedirs(import_dir)
    logger.info(f"Created import directory: {import_dir}")

# Create a test image with a gradient and some shapes
def create_test_image(filename="test_texture.png", size=(512, 512)):
    """
    Create a test image with a gradient background and various shapes.
    
    # This function creates a test image. It's not rocket science.
    # Just a gradient with some shapes slapped on top. Art critics, look away.
    """
    # Create a gradient background
    gradient = np.zeros((size[1], size[0]), dtype=np.uint8)
    for y in range(size[1]):
        for x in range(size[0]):
            gradient[y, x] = int(255 * (x / size[0]))
            
    # Convert to PIL Image
    image = Image.fromarray(gradient)
    
    # Add some shapes
    draw = ImageDraw.Draw(image)
    
    # Draw a circle
    draw.ellipse((100, 100, 400, 400), fill=200)
    
    # Draw some rectangles
    draw.rectangle((50, 50, 150, 150), fill=150)
    draw.rectangle((350, 350, 450, 450), fill=100)
    
    # Draw some lines
    for i in range(0, 500, 50):
        draw.line((0, i, i, 0), fill=255, width=5)
        
    # Save the image
    output_path = os.path.join(import_dir, filename)
    image.save(output_path)
    logger.info(f"Test image created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_test_image() 