#!/usr/bin/env python3
"""
Basic usage example for the cimseg package.

"""

import cimseg

#%%

image_file = "carrier.jpg"

segments, image, grid_lines = cimseg.carrier2samples(image_file, rotate=True)

# Visualize result

cimseg.visualize_segmentation(image, segments, grid_lines)