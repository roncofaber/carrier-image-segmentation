# Carrier Image Segmentation (cimseg)

A Python package for automatically segmenting carrier tray images into individual sample segments. This tool is designed to extract 16 individual samples from a 4×4 grid carrier tray using computer vision techniques.

## Features

- **Automatic carrier detection**: Isolates the carrier tray from the background
- **Grid alignment**: Uses cross-detection algorithms for precise grid positioning
- **Sample extraction**: Extracts 16 individual segments (A1-D4 well format)
- **Visualization tools**: Display segmentation results with overlays
- **Configurable parameters**: Adjust thresholds and detection parameters

## Installation

### Install from source

```bash
# Clone the repository
git clone https://github.com/roncofaber/carrier-image-segmentation.git
cd carrier-image-segmentation

# Install in development mode
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

### Dependencies

- Python ≥ 3.8
- NumPy ≥ 1.20.0
- SciPy ≥ 1.7.0
- scikit-image ≥ 0.18.0
- matplotlib ≥ 3.3.0

## Quick Start

```python
import cimseg
import numpy as np
from skimage import io

# Load your carrier tray image
image = io.imread('path/to/your/carrier_image.jpg')

# Extract segments from the carrier
segments, processed_image, grid_lines = cimseg.carrier2samples(image)

# Access individual segments
segment_A1 = segments['A1']['segment']  # Top-left sample
segment_D4 = segments['D4']['segment']  # Bottom-right sample

# Visualize the segmentation results
cimseg.visualize_segmentation(processed_image, segments, grid_lines)
```

## Usage

### Basic Segmentation

```python
import cimseg

# Basic usage with default parameters
segments, image, grid = cimseg.carrier2samples(input_image)

# Each segment contains:
for well_id, segment_data in segments.items():
    segment_image = segment_data['segment']      # The extracted image
    well_position = segment_data['carrier_well'] # e.g., 'A1', 'B2', etc.
    row, col = segment_data['row'], segment_data['col']  # Grid position (0-3)
    shape = segment_data['shape']               # Image dimensions
    x_range = segment_data['x_range']           # (x_start, x_end)
    y_range = segment_data['y_range']           # (y_start, y_end)
```

### Advanced Configuration

```python
# Fine-tune segmentation parameters
segments, image, grid = cimseg.carrier2samples(
    input_image,
    threshold=0.25,        # Carrier detection threshold (0-1)
    max_object_size=300,   # Max noise object size to remove
    peak_height=0.7,       # Peak detection sensitivity
    peak_distance=450,     # Minimum distance between peaks
    cross_size=350,        # Cross detection area size
    rotate=True            # Enable automatic rotation correction
)
```

### Visualization

```python
# Display segmentation results
cimseg.visualize_segmentation(processed_image, segments, grid_lines)

# This creates two plots:
# 1. Original image with grid overlay and segment labels
# 2. 4×4 grid showing all extracted segments
```

## Well Naming Convention

Segments are labeled using standard microplate notation:
- **Rows**: A, B, C, D (top to bottom)
- **Columns**: 1, 2, 3, 4 (left to right)
- **Wells**: A1, A2, A3, A4, B1, B2, ..., D3, D4

```
A1  A2  A3  A4
B1  B2  B3  B4
C1  C2  C3  C4
D1  D2  D3  D4
```

## Algorithm Overview

1. **Carrier Detection**: Isolates the dark carrier frame from the background
2. **Image Preprocessing**: Converts to grayscale and applies rotation correction
3. **Cross Detection**: Locates alignment crosses in the carrier grid
4. **Grid Calculation**: Extrapolates 4×4 grid boundaries from 3×3 cross positions
5. **Segment Extraction**: Crops individual sample areas based on grid

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `threshold` | 0.31 | Carrier detection threshold (0-1) |
| `max_object_size` | 500 | Max size of objects to remove as noise |
| `peak_height` | 0.6 | Minimum peak height for detection |
| `peak_distance` | 400 | Minimum distance between detected peaks |
| `cross_size` | 400 | Size of cross search area |
| `cross_width` | 20 | Width of cross detection bars |
| `rotate` | False | Enable automatic rotation correction |

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests (if available)
pytest

# Code formatting
black cimseg/
isort cimseg/
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
