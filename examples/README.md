# Examples

This directory contains example scripts demonstrating how to use the `cimseg` package for carrier image segmentation.

## Files

- **`basic_usage.py`** - Complete example showing the main workflow
- **`sample_carrier.jpg`** - Put your sample carrier tray image here (optional)
- **`output_segments/`** - Directory created when saving individual segments

## Running the Examples

### Prerequisites

Make sure you have the package installed:
```bash
pip install -e .
```

### Basic Usage Example

```bash
# Using your own image
python examples/basic_usage.py path/to/your/carrier_image.jpg

# Or place a sample image at examples/sample_carrier.jpg and run
python examples/basic_usage.py
```

### What the Example Demonstrates

1. **Loading Images** - How to load carrier tray images
2. **Basic Segmentation** - Extract 16 segments using default parameters
3. **Advanced Segmentation** - Fine-tune parameters for better results
4. **Accessing Results** - How to work with the segmentation output
5. **Visualization** - Display results with grid overlay
6. **Saving Segments** - Export individual segments as image files

### Example Output

```
CIMSEG - Carrier Image Segmentation Example
==================================================
Loading image from: examples/sample_carrier.jpg
✓ Image loaded successfully: (2000, 3000, 3)

1. Extracting segments with default parameters...
✓ Extracted 16 segments

2. Segment information:
--------------------------------------------------
A1: 450×600 pixels
A2: 450×600 pixels
A3: 450×600 pixels
A4: 450×600 pixels
B1: 450×600 pixels
...
D4: 450×600 pixels

3. Accessing specific segments:
✓ A1 segment: (450, 600, 3)
✓ D4 segment: (450, 600, 3)

4. Displaying visualization...
[matplotlib windows will open showing segmentation results]

Save individual segments to files? (y/n): y

5. Saving segments to examples/output_segments/
✓ Saved A1 -> examples/output_segments/segment_A1.png
✓ Saved A2 -> examples/output_segments/segment_A2.png
...
✓ All segments saved to examples/output_segments/

✓ Example completed successfully!
```

## Image Requirements

Your carrier tray images should:
- Be in a common format (JPG, PNG, TIFF, etc.)
- Contain a dark carrier frame with visible alignment crosses
- Have samples arranged in a 4×4 grid pattern
- Be reasonably well-lit and in focus

## Parameter Tuning

If the default parameters don't work well for your images, try adjusting:

- **`threshold`** (0.2-0.4) - Carrier detection sensitivity
- **`peak_height`** (0.5-0.8) - Cross detection sensitivity
- **`peak_distance`** (300-500) - Minimum spacing between crosses
- **`cross_size`** (300-500) - Cross search area size
- **`rotate=True`** - Enable automatic rotation correction

See the advanced example in `basic_usage.py` for reference.

## Creating Additional Examples

To create your own example:

1. Create a new Python file in this directory
2. Import the package: `import cimseg`
3. Use the main function: `cimseg.carrier2samples(image)`
4. Add visualization: `cimseg.visualize_segmentation(...)`

## Sample Data

To test the examples, place your carrier tray image as:
```
examples/sample_carrier.jpg
```

Or specify any image path when running the example script.