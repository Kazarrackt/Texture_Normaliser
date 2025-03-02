# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.4 - 2025-03-03
# ---

import os
import sys

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from src directory
from src.texture_processor import processor
from src.logger import logger

def test_processor():
    """Test the texture processor with the test image."""
    # Path to the test image
    test_image_path = "./import/test_texture.png"
    
    # Check if the test image exists
    if not os.path.exists(test_image_path):
        logger.error(f"Test image not found: {test_image_path}")
        return False
        
    # Process the test image
    logger.info(f"Processing test image: {test_image_path}")
    result = processor.process_image(test_image_path)
    
    # Check the result
    if result["success"]:
        logger.info(f"Test successful! Output directory: {result['output_dir']}")
        logger.info(f"Generated files: {list(result['results'].keys())}")
        return True
    else:
        logger.error(f"Test failed: {result.get('error', 'Unknown error')}")
        return False

if __name__ == "__main__":
    # Run the test
    success = test_processor()
    print(f"Test {'succeeded' if success else 'failed'}") 