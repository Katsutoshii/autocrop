"""Autocrop tool

This Python script consumes a list of input directories of PNG files and crops them.
The user must specify a pivot for each group of directories. This pivot location is guaranteed to be
Preserved during the crop. For example, (0.5, 0.5) ensures that the pivot is centered on the image.
Use config.py to edit the input config.

Email: joshikatsu@gmail.com
"""
from pathlib import Path
from typing import List, Tuple
from autocrop import crop_images, Pivot
import config


def main(root_dir: str, output_dir: str, inputs: List[Tuple[Pivot, List[List[str]]]]):
    root_path: Path = Path(root_dir)
    output_path: Path = Path(output_dir)
    for pivot, group in inputs:
        for input_dirs in group:
            crop_images(root_path, input_dirs, pivot, output_path)


if __name__ == "__main__":
    main(config.root_dir, config.output_dir, config.inputs)
