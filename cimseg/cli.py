#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command-line interface for cimseg."""

import argparse
import os
import sys

from skimage import img_as_ubyte, io

from .carrier2samples import carrier2samples


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="cimseg",
        description="Extract 16 samples from a carrier tray image.",
    )
    parser.add_argument("image", help="Path to the tray image")
    parser.add_argument("-o", "--output", default=".", help="Output directory (default: current directory)")
    parser.add_argument("--rotate", action="store_true", help="Auto-rotate the tray to correct tilt")
    parser.add_argument("--threshold", type=float, default=0.31, help="Threshold for holder detection")
    parser.add_argument("--peak-height", type=float, default=0.6, help="Minimum peak height for row/cross detection")
    parser.add_argument("--peak-distance", type=int, default=400, help="Minimum distance between peaks")
    parser.add_argument("--preview", action="store_true", help="Also save a grid-overlay preview image")
    args = parser.parse_args(argv)

    os.makedirs(args.output, exist_ok=True)
    stem = os.path.splitext(os.path.basename(args.image))[0]

    segments, image, grid_lines = carrier2samples(
        args.image,
        threshold=args.threshold,
        peak_height=args.peak_height,
        peak_distance=args.peak_distance,
        rotate=args.rotate,
    )

    for well, data in segments.items():
        out_path = os.path.join(args.output, f"{stem}_{well}.png")
        io.imsave(out_path, img_as_ubyte(data["segment"]))
    print(f"Saved {len(segments)} segments to {args.output}")

    if args.preview:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(image)
        for x in grid_lines["x_grid"]:
            ax.axvline(x=x, color="blue", alpha=0.7, linewidth=2)
        for y in grid_lines["y_grid"]:
            ax.axhline(y=y, color="blue", alpha=0.7, linewidth=2)
        for well, data in segments.items():
            xc = sum(data["x_range"]) / 2
            yc = sum(data["y_range"]) / 2
            ax.text(xc, yc, well, ha="left", va="top", color="white", fontsize=10, fontweight="bold")
        ax.axis("off")

        preview_path = os.path.join(args.output, f"{stem}_preview.png")
        fig.savefig(preview_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"Saved preview to {preview_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
