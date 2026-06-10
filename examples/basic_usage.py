#!/usr/bin/env python3
"""
Basic usage example for the cimseg package.

Processes all carrier images in data/ and saves grid overlay and
segment plots to output/.
"""

import os
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cimseg

DATA_DIR   = os.path.join(os.path.dirname(__file__), "data")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

image_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.jpg")))

for image_path in image_files:
    name = os.path.splitext(os.path.basename(image_path))[0]
    print(f"Processing {name}...")

    segments, image, grid_lines = cimseg.carrier2samples(image_path, rotate=True)

    # Grid overlay
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image)
    for x in grid_lines["x_grid"]:
        ax.axvline(x=x, color="blue", linestyle="-", alpha=0.7, linewidth=2)
    for y in grid_lines["y_grid"]:
        ax.axhline(y=y, color="blue", linestyle="-", alpha=0.7, linewidth=2)
    for well_idx, seg in segments.items():
        ax.text(seg["x_range"][0] + 50, seg["y_range"][0] + 50, well_idx,
                ha="left", va="top", color="white", fontsize=10, fontweight="bold")
    ax.set_title(name)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f"{name}_grid.png"), dpi=100, bbox_inches="tight")
    plt.close(fig)

    # Individual segments
    fig, axes = plt.subplots(4, 4, figsize=(12, 12))
    fig.suptitle(name)
    for well_idx, seg in segments.items():
        ax = axes[seg["row"], seg["col"]]
        ax.imshow(seg["segment"])
        ax.set_title(well_idx, fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, f"{name}_segments.png"), dpi=100, bbox_inches="tight")
    plt.close(fig)

    print(f"  -> saved {name}_grid.png and {name}_segments.png")

print(f"\nDone. Results in {OUTPUT_DIR}/")
