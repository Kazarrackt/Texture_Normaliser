# Texture Normaliser

A powerful tool for generating normal maps, bump maps, and AO/roughness maps from texture images.

![Texture Normaliser Logo](../assets/logo.png)

## Features

- Generate normal maps using Sobel filter
- Generate bump maps using histogram equalization
- Generate AO/roughness maps (optional)
- Modern, user-friendly interface
- Batch processing of multiple files
- Configurable export directory
- Dark and light theme support

## Installation

### Option 1: Using the Executable (Windows)

1. Download the latest release from the releases page
2. Extract the ZIP file to a location of your choice
3. Run `TextureNormaliser.exe`

### Option 2: From Source

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Usage

### Basic Usage

1. Launch the application
2. Select files or a folder containing texture images
3. Configure the options as needed
4. Click "Process" to generate the maps
5. Access the generated maps in the export directory

### Options

- **Enable Normal Map**: Generate normal maps using the Sobel filter
- **Enable Bump Map**: Generate bump maps using histogram equalization
- **Enable AO/Roughness**: Generate ambient occlusion/roughness maps
- **Kernel Size**: Set the Sobel filter kernel size (3, 5, 7, or 9)
- **Export Directory**: Set the directory where generated maps will be saved
- **Theme**: Choose between Dark, Light, or System theme

### Output

For each processed image, the following files will be generated in the export directory:

- `<filename>_original.png`: A copy of the original image
- `<filename>_normal_map.png`: The generated normal map (if enabled)
- `<filename>_bump_map.png`: The generated bump map (if enabled)
- `<filename>_ao_roughness.png`: The generated AO/roughness map (if enabled)

## Command Line Usage

The texture processor can also be used from the command line:

```
python -m src.texture_processor <input_path>
```

Where `<input_path>` can be a file or directory.

## Testing

The project includes scripts for testing and demonstration in the `tests` directory:

### Generate Test Image

To create a test texture image with a gradient and shapes:

```
python tests/create_test_image.py
```

This will create a test image in the `import` directory.

### Test Processor

To test the core texture processing functionality:

```
python tests/test_processor.py
```

This will process the test image and verify that the normal map and bump map are generated correctly.

For more information about the tests, see the [tests README](tests/README.md).

## Development

### Project Structure

- `main.py`: Main application entry point
- `src/`: Core application modules
  - `texture_processor.py`: Core texture processing functionality
  - `config.py`: Configuration management
  - `logger.py`: Logging functionality
- `assets/`: Application assets (images, icons)
- `docs/`: Documentation files
  - `README.md`: This file
  - `changelog.txt`: Version history and changes
- `tests/`: Test and debugging utilities
  - `create_test_image.py`: Generate test images
  - `test_processor.py`: Test the texture processor

### Building the Executable

To build the executable:

```
pyinstaller --onefile --windowed --icon=assets/logo.ico --add-data "assets/logo.png;assets" main.py
```

Or use the provided spec file:

```
python -m PyInstaller TextureNormaliser.spec
```

## License

© 2025 KazLabs Media Group - Made with ♥ by Liam Sorensen 