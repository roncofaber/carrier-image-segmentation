# Examples

This directory contains example scripts and data for the `cimseg` package.

## Structure

```
examples/
├── basic_usage.py      # Main example script
├── data/               # Input carrier images
│   ├── carrier_01.jpg
│   ├── carrier_02.jpg
│   └── ...
└── output/             # Generated plots (git-ignored)
```

## Running

```bash
cd examples/
python basic_usage.py
```

Processes every `.jpg` in `data/` and writes two files per image to `output/`:

- `<name>_grid.png` — full image with grid overlay and well labels
- `<name>_segments.png` — 4×4 grid of extracted well segments

## Adding new images

Drop any carrier tray `.jpg` into `data/` and re-run the script.

## Parameter tuning

If the default parameters don't work well for your images, pass keyword
arguments to `carrier2samples`:

| Parameter | Default | Effect |
|---|---|---|
| `threshold` | 0.31 | Carrier frame detection sensitivity |
| `peak_height` | 0.6 | Minimum cross detection intensity |
| `peak_distance` | 400 | Minimum pixel distance between crosses |
| `cross_size` | 400 | Cross search window size (px) |
| `rotate` | False | Enable automatic tilt correction |
