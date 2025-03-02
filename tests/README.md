# Texture Normaliser Tests

This directory contains test and debugging utilities for the Texture Normaliser application.

## Available Tests

### Create Test Image

Generates a test image with a gradient and various shapes for testing the texture processor.

```bash
python tests/create_test_image.py
```

This will create a test image at `./import/test_texture.png`.

### Test Processor

Tests the core texture processing functionality using the test image.

```bash
python tests/test_processor.py
```

This will process the test image and verify that the normal map and bump map are generated correctly.

## Project Structure

The tests are designed to work with the new project structure:

```
/
├── main.py              # Main entry point
├── src/                 # Core application modules
│   ├── texture_processor.py
│   ├── config.py
│   └── logger.py
├── assets/              # Application assets
├── docs/                # Documentation
└── tests/               # Test utilities
    ├── create_test_image.py
    ├── test_processor.py
    └── README.md
```

## Notes

- These tests are designed for development and debugging purposes.
- The test image generator creates a simple image with predictable patterns to test the processor.
- The processor test verifies that the core functionality works correctly.
- The tests import modules from the `src` directory.

© 2025 Kazlabs - Made with ♥️ by Liam Sorensen 