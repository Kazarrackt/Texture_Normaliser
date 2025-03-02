# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.4 - 2025-03-03
# ---

import os
import json
from src.logger import logger

class Config:
    """
    Configuration class for the Texture Normaliser application.
    
    # This class manages settings. It's basically just a glorified dictionary.
    # But hey, at least it saves to a JSON file, so that's something I guess.
    """
    DEFAULT_CONFIG = {
        "enable_normal_map": True,
        "enable_bump_map": True,
        "enable_ao_roughness": False,
        "export_directory": "./export/",
        "theme": "dark",
        "sobel_kernel_size": 5,
        "last_import_directory": "./import/"
    }
    
    def __init__(self, config_file="config.json"):
        """Initialize the configuration."""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """
        Load configuration from file or create default if it doesn't exist.
        
        # Tries to load a config file. If it fails, we'll just use defaults.
        # Because who needs error handling when you can just ignore problems?
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    logger.info(f"Configuration loaded from {self.config_file}")
                    
                    # Ensure all default keys exist
                    for key, value in self.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                            
                    return config
            else:
                logger.info(f"Configuration file {self.config_file} not found, creating default")
                self.save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, config=None):
        """
        Save configuration to file.
        
        # Saves settings to a file. Will probably fail silently if the disk is full.
        # But that's a problem for future you, not current me.
        """
        if config is None:
            config = self.config
            
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value and save to file."""
        self.config[key] = value
        return self.save_config()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save_config()

# Create a global config instance
config = Config()

if __name__ == "__main__":
    # Test the config
    print(f"Current config: {config.config}")
    config.set("theme", "light")
    print(f"Updated config: {config.config}")
    config.reset_to_defaults()
    print(f"Reset config: {config.config}") 