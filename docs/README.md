# Texture Normaliser

A tool for generating normal maps and other texture maps from source images.

## Features

- Generate normal maps from texture images
- Generate bump maps from texture images
- Generate ambient occlusion maps
- Generate roughness maps
- Batch processing support
- Configurable export directory
- Dark/Light theme support

## Installation

### Option 1: Download the executable
Download the latest release from the releases page and run the executable.

### Option 2: Run from source
1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Run the application:
```
python main.py
```

## Project Structure

```
Texture_Normaliser/
├── assets/            # Image assets and resources
├── docs/              # Documentation files
├── src/               # Core Python modules
│   ├── config.py      # Configuration management
│   ├── logger.py      # Logging system
│   └── texture_processor.py  # Texture processing logic
├── tests/             # Test scripts
│   ├── create_test_image.py  # Test image generator
│   └── test_processor.py     # Processor test script
├── main.py            # Main application entry point
├── TextureNormaliser.spec  # PyInstaller specification
└── requirements.txt   # Python dependencies
```

## Usage

1. Launch the application
2. Select a source texture image or directory
3. Configure processing options
4. Click "Process" to generate texture maps
5. View the generated maps in the export directory

## Configuration

The application stores configuration in `config.json`. You can modify the following settings:

- Export directory
- Default kernel size
- UI theme (dark/light)
- Recent files list

## Testing

### Generate Test Image

To create a test image for testing purposes:

```
python tests/create_test_image.py
```

This will generate a test texture image in the `import/` directory.

### Test Processor

To test the core texture processing functionality:

```
python tests/test_processor.py
```

This will process the test image and verify that the processor is working correctly.

## Building the Executable

To build the executable:

```
python -m PyInstaller TextureNormaliser.spec
```

The executable will be created in the `dist/` directory.

## License

© 2025 KazLabs Media Group - Made with ♥ by Liam Sorensen 