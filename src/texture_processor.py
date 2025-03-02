# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.4 - 2025-03-03
# ---

import os
import uuid
from PIL import Image
import numpy as np
import cv2
from src.logger import logger
from src.config import config

class TextureProcessor:
    """
    Core texture processing class for generating normal maps, bump maps, and AO/roughness maps.
    
    # This class does all the heavy lifting. It's basically just a wrapper around
    # OpenCV functions, but don't tell anyone or they'll realize how simple this is.
    """
    
    def __init__(self):
        """Initialize the texture processor."""
        self.kernel_size = config.get("sobel_kernel_size", 5)
        logger.info(f"TextureProcessor initialized with kernel size {self.kernel_size}")
        
    def set_kernel_size(self, size):
        """Set the Sobel kernel size."""
        if size % 2 == 1 and size >= 3:  # Must be odd and at least 3
            self.kernel_size = size
            config.set("sobel_kernel_size", size)
            logger.info(f"Kernel size set to {size}")
            return True
        else:
            logger.error(f"Invalid kernel size: {size}. Must be odd and >= 3")
            return False
            
    def process_image(self, input_path, output_dir=None):
        """
        Process an image to generate normal map, bump map, and AO/roughness map.
        
        # Takes an image, applies some filters, and spits out some other images.
        # It's like Instagram, but for game developers who don't know how to use Substance.
        """
        if output_dir is None:
            output_dir = config.get("export_directory", "./export/")
            
        try:
            # Ensure output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.info(f"Created output directory: {output_dir}")
                
            # Load the image
            logger.info(f"Processing image: {input_path}")
            image = Image.open(input_path)
            image_np = np.array(image)
            
            # Get image details
            image_size = os.path.getsize(input_path)
            image_dimensions = image.size
            logger.info(f"Image size: {image_size} bytes, dimensions: {image_dimensions}")
            
            # Create a folder for the output using the base filename
            base_filename = os.path.splitext(os.path.basename(input_path))[0]
            image_output_dir = os.path.join(output_dir, base_filename)
            if not os.path.exists(image_output_dir):
                os.makedirs(image_output_dir)
                
            # Save a copy of the original image
            original_output_path = os.path.join(image_output_dir, f"{base_filename}_original.png")
            image.save(original_output_path)
            logger.info(f"Saved original image to: {original_output_path}")
            
            # Convert to grayscale
            if len(image_np.shape) == 3 and image_np.shape[2] >= 3:
                if image_np.shape[2] == 4:  # RGBA
                    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGBA2GRAY)
                else:  # RGB
                    gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            else:  # Already grayscale
                gray_image = image_np
                
            results = {}
                
            # Generate Normal Map if enabled
            if config.get("enable_normal_map", True):
                normal_map = self._generate_normal_map(gray_image)
                normal_map_output_path = os.path.join(image_output_dir, f"{base_filename}_normal_map.png")
                Image.fromarray(normal_map).save(normal_map_output_path)
                logger.info(f"Saved normal map to: {normal_map_output_path}")
                results["normal_map"] = normal_map_output_path
                
            # Generate Bump Map if enabled
            if config.get("enable_bump_map", True):
                bump_map = self._generate_bump_map(gray_image)
                bump_map_output_path = os.path.join(image_output_dir, f"{base_filename}_bump_map.png")
                Image.fromarray(bump_map).save(bump_map_output_path)
                logger.info(f"Saved bump map to: {bump_map_output_path}")
                results["bump_map"] = bump_map_output_path
                
            # Generate AO/Roughness Map if enabled
            if config.get("enable_ao_roughness", False):
                ao_roughness_map = self._generate_ao_roughness_map(gray_image)
                ao_roughness_output_path = os.path.join(image_output_dir, f"{base_filename}_ao_roughness.png")
                Image.fromarray(ao_roughness_map).save(ao_roughness_output_path)
                logger.info(f"Saved AO/roughness map to: {ao_roughness_output_path}")
                results["ao_roughness"] = ao_roughness_output_path
                
            logger.info(f"Successfully processed image: {input_path}")
            return {
                "success": True,
                "input_path": input_path,
                "output_dir": image_output_dir,
                "results": results
            }
                
        except Exception as e:
            logger.exception(f"Error processing image {input_path}: {e}")
            return {
                "success": False,
                "input_path": input_path,
                "error": str(e)
            }
            
    def _generate_normal_map(self, gray_image):
        """
        Generate a normal map from a grayscale image.
        
        # Applies the Sobel operator to create a normal map.
        # It's basically just calculating derivatives, but we'll pretend it's magic.
        """
        # Generate Normal Map using Sobel filter
        sobelx = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=self.kernel_size)
        sobely = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=self.kernel_size)
        
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
        
        return normal_map
        
    def _generate_bump_map(self, gray_image):
        """
        Generate a bump map from a grayscale image.
        
        # Applies histogram equalization to make a bump map.
        # It's literally just one line of code, but we'll wrap it in a function
        # to make it look like we're doing something complex.
        """
        # Generate Bump Map using grayscale with histogram equalization
        bump_map = cv2.equalizeHist(gray_image)
        
        return bump_map
        
    def _generate_ao_roughness_map(self, gray_image):
        """
        Generate an ambient occlusion / roughness map from a grayscale image.
        
        # This is basically just inverting the image and applying some filters.
        # But we'll call it "AO/roughness" to sound fancy and technical.
        """
        # Invert the grayscale image for AO effect
        inverted = 255 - gray_image
        
        # Apply bilateral filter to smooth while preserving edges
        filtered = cv2.bilateralFilter(inverted, 9, 75, 75)
        
        # Apply adaptive histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        ao_roughness = clahe.apply(filtered)
        
        return ao_roughness
        
    def process_directory(self, input_dir, output_dir=None):
        """
        Process all images in a directory.
        
        # Processes a whole directory of images at once.
        # Because doing them one at a time is for people with patience.
        """
        if output_dir is None:
            output_dir = config.get("export_directory", "./export/")
            
        results = {
            "success": [],
            "failed": []
        }
        
        try:
            # Ensure input directory exists
            if not os.path.exists(input_dir):
                logger.error(f"Input directory does not exist: {input_dir}")
                return {
                    "success": False,
                    "error": f"Input directory does not exist: {input_dir}"
                }
                
            # Process each image in the directory
            for filename in os.listdir(input_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    input_path = os.path.join(input_dir, filename)
                    result = self.process_image(input_path, output_dir)
                    
                    if result["success"]:
                        results["success"].append(result)
                    else:
                        results["failed"].append(result)
                        
            logger.info(f"Processed {len(results['success'])} images successfully, {len(results['failed'])} failed")
            return {
                "success": True,
                "input_dir": input_dir,
                "output_dir": output_dir,
                "results": results
            }
                
        except Exception as e:
            logger.exception(f"Error processing directory {input_dir}: {e}")
            return {
                "success": False,
                "input_dir": input_dir,
                "error": str(e)
            }

# Create a global processor instance
processor = TextureProcessor()

if __name__ == "__main__":
    # Test the processor
    import sys
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if os.path.isfile(input_path):
            result = processor.process_image(input_path)
            print(f"Processing result: {result['success']}")
        elif os.path.isdir(input_path):
            result = processor.process_directory(input_path)
            print(f"Processing result: {result['success']}, {len(result['results']['success'])} succeeded, {len(result['results']['failed'])} failed")
        else:
            print(f"Invalid input path: {input_path}")
    else:
        print("Usage: python texture_processor.py <input_path>")
        print("  <input_path> can be a file or directory") 