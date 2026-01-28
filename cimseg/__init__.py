"""
Carrier Image Segmentation (cimseg) - A package for segmenting carrier tray images into individual samples.

This package provides functionality to:
- Detect and isolate carrier trays from images
- Extract 16 individual segments from a 4x4 grid
- Visualize segmentation results

Main function:
    carrier2samples: Extract segments from tray images using cross detection

Modules:
    segment: Core segmentation algorithms
    utils: Utility functions
    plot: Visualization tools
"""

from .carrier2samples import carrier2samples
from .plot import visualize_segmentation

__version__ = "0.1.0"
__author__ = "roncofaber"

__all__ = [
    'carrier2samples',
    'visualize_segmentation'
]