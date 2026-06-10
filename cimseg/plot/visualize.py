#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 17:52:18 2026

@author: roncofaber
"""

def visualize_segmentation(image, segments, grid_lines):
    """
    Visualize the segmentation result with grid overlay.

    Parameters
    ----------
    image : ndarray
        Cropped grayscale image
    segments : list
        List of 16 segments
    segment_info : list
        List of segment metadata
    grid_lines : dict
        Grid line coordinates
    """
    import matplotlib.pyplot as plt

    # Main image with grid overlay
    plt.figure(figsize=(12, 8))
    plt.imshow(image, cmap='gray')

    # Draw grid lines
    for x in grid_lines['x_grid']:
        plt.axvline(x=x, color='blue', linestyle='-', alpha=0.7, linewidth=2)
    for y in grid_lines['y_grid']:
        plt.axhline(y=y, color='blue', linestyle='-', alpha=0.7, linewidth=2)

    # Label segments
    for well_idx, segment in segments.items():
        x_center = (segment['x_range'][0] + segment['x_range'][1]) / 2
        y_center = (segment['y_range'][0] + segment['y_range'][1]) / 2
        text_color = 'white'
        plt.text(x_center, y_center, f"{well_idx}",
                ha='left', va='top', color=text_color, fontsize=10, fontweight='bold')

    plt.title('4x4 Grid Segmentation using Cross Detection')
    plt.axis('off')
    plt.show()

    # Individual segments
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    fig.suptitle('16 Extracted Segments', fontsize=14)

    for well_idx, segment in segments.items():
        row, col = segment['row'], segment['col']
        ax = axes[row, col]

        ax.imshow(segment["segment"], cmap='gray')
        ax.set_title(f'{well_idx}', fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.show()