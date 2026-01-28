#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 13:55:47 2026

@author: roncofaber
"""

# scientific computing
import numpy as np

# image recognition
from skimage import color

# local imports
from .segment import isolate_carrier, find_horizontal_peaks, find_cross_peaks_at_y
from .utils import number_to_well

#%%

def carrier2samples(image, threshold=0.31, max_object_size=500, bar_height=20, bar_width=2000,
                     peak_height=0.6, peak_distance=400, middle_start=500, middle_end=3000,
                     cross_size=400, cross_width=20, rotate=False):
    """
    Extract 16 segments from a tray image using cross detection for grid alignment.

    Parameters
    ----------
    image : ndarray
        Input tray image (RGB or grayscale)
    threshold : float, optional
        Threshold for holder detection (default: 0.31)
    max_object_size : int, optional
        Maximum object size for noise removal (default: 500)
    bar_height : int, optional
        Height of horizontal scan bar (default: 20)
    bar_width : int, optional
        Width of horizontal scan bar (default: 2000)
    peak_height : float, optional
        Minimum peak height for detection (default: 0.6)
    peak_distance : int, optional
        Minimum distance between peaks (default: 400)
    middle_start : int, optional
        Start of middle region for peak search (default: 500)
    middle_end : int, optional
        End of middle region for peak search (default: 3000)
    cross_size : int, optional
        Size of cross search area (default: 400)
    cross_width : int, optional
        Width of cross search bar (default: 20)

    Returns
    -------
    segments : list
        List of 16 image segments (4x4 grid)
    segment_info : list
        List of dictionaries with segment metadata
    cropped_image : ndarray
        The cropped and processed image
    grid_lines : dict
        Dictionary with 'x_grid' and 'y_grid' coordinates
    """

    # Step 1: Detect and crop holder
    image = isolate_carrier(image, threshold=threshold,
                            max_object_size=max_object_size, rotate=rotate)

    # Step 3: Convert to grayscale (now on potentially rotated image)
    image_gray = color.rgb2gray(image)

    # Step 4: Find horizontal peaks (rows with samples)
    three_peaks, _ = find_horizontal_peaks(
        image_gray, bar_height=bar_height, bar_width=bar_width,
        peak_height=peak_height, peak_distance=peak_distance,
        middle_start=middle_start, middle_end=middle_end)

    # Step 5: Find cross positions at each y-position
    cross_coordinates = find_cross_peaks_at_y(
        image_gray, three_peaks, cross_size=cross_size, cross_width=cross_width,
        peak_height=peak_height, peak_distance=peak_distance)

    # Step 6: Calculate grid boundaries from cross positions
    y_sorted = sorted(cross_coordinates[:, 1])
    x_sorted = sorted(cross_coordinates[:, 0])

    # Average positions for the 3x3 cross grid
    y_str = int(np.mean(y_sorted[:3]))
    y_mid = int(np.mean(y_sorted[3:6]))
    y_end = int(np.mean(y_sorted[6:9]))

    x_str = int(np.mean(x_sorted[:3]))
    x_mid = int(np.mean(x_sorted[3:6]))
    x_end = int(np.mean(x_sorted[6:9]))

    # Calculate spacing and extrapolate to 4x4 grid
    x_spacing = (x_end - x_str) / 2
    y_spacing = (y_end - y_str) / 2

    x_grid = [
        int(x_str - x_spacing),  # Left boundary
        x_str,                   # First cross column
        x_mid,                   # Middle cross column
        x_end,                   # Right cross column
        int(x_end + x_spacing)   # Right boundary
    ]

    y_grid = [
        int(y_str - y_spacing),  # Top boundary
        y_str,                   # First cross row
        y_mid,                   # Middle cross row
        y_end,                   # Bottom cross row
        int(y_end + y_spacing)   # Bottom boundary
    ]

    # Step 7: Extract 16 segments
    segments = dict()
    
    idx = 0
    for row in range(4):
        for col in range(4):
            
            well_idx = number_to_well(idx)
            segments[well_idx] = dict()
            
            # Define boundaries for this segment
            x_start = max(0, x_grid[col])
            x_end = min(image_gray.shape[1], x_grid[col + 1])
            y_start = max(0, y_grid[row])
            y_end = min(image_gray.shape[0], y_grid[row + 1])

            # Extract the segment
            segment = image[y_start:y_end, x_start:x_end]
            
            # Store data in dict
            segments[well_idx].update(
                {
                    "segment" : segment,
                    "carrier_well" : number_to_well(idx),
                    'row': row,
                    'col': col,
                    'x_range': (x_start, x_end),
                    'y_range': (y_start, y_end),
                    'shape': segment.shape,
                })
            idx += 1
            
    grid_lines = {'x_grid': x_grid, 'y_grid': y_grid}

    return segments, image, grid_lines


