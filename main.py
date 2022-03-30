"""Autocrop tool

This Python script consumes a list of input directories of PNG files and crops them.
The user must specify a pivot for each group of directories. This pivot location is guaranteed to be
Preserved during the crop. For example, (0.5, 0.5) ensures that the pivot is centered on the image.
Use config.py to edit the input config.

Email: joshikatsu@gmail.com
"""

from typing import Optional, Tuple, List
import glob
from dataclasses import dataclass
import math
from pathlib import Path
from PIL import Image  # type: ignore
import config
import sys


X: int = 0
Y: int = 1

Vec2 = Tuple[int, int]


def round_down(v: int, n: int) -> int:
    """Round v to the nearest multiple of n.
    `round(63, 4) -> 60`
    """
    return n * math.floor(v / n)


def round_up(v: int, n: int) -> int:
    """Round v to the nearest multiple of n.
    `round(63, 4) -> 64`
    """
    return n * math.ceil(v / n)


@dataclass
class BoundingBox:
    min_x: int
    min_y: int
    max_x: int
    max_y: int

    def grow_to_fit_image(self, image: Image):
        """Grow the bounding box to fit all populated pixels in this image."""
        min_x, min_y, max_x, max_y = image.getbbox()
        self.min_x = min(min_x, self.min_x)
        self.min_y = min(min_y, self.min_y)
        self.max_x = max(max_x, self.max_x)
        self.max_y = max(max_y, self.max_y)

    def round_bounds(self, n: int):
        """Rounds bounds the nearest nth pixel"""
        self.min_x = round_down(self.min_x, n)
        self.min_y = round_down(self.min_y, n)
        self.max_x = round_up(self.max_x, n)
        self.max_y = round_up(self.max_y, n)

    def __str__(self) -> str:
        return f"({self.min_x}, {self.min_y}) ({self.max_x}, {self.max_y})"

    def crop(self, image: Image) -> Image:
        """Crops an image using this bounding box."""
        return image.crop((self.min_x, self.min_y, self.max_x, self.max_y))


def getbbox(input_path: Path, pivot: Vec2) -> Optional[BoundingBox]:
    """Get the bounding box that covers all images in a directory and overwrites with a cropped version."""
    bb: Optional[BoundingBox] = None
    for infile in glob.glob(f"{input_path}/**/*.png", recursive=True):
        print("  Processing", infile)
        with Image.open(infile) as image:
            # For first image, initialize the bounds.
            if bb is None:
                pivot_px: Vec2 = (
                    int(image.width * pivot[X]), int(image.height * pivot[Y]))
                bb = BoundingBox(
                    pivot_px[X], pivot_px[Y], pivot_px[X], pivot_px[Y])

            bb.grow_to_fit_image(image)
            print("    Bounding box:", bb)

    if bb is None:
        print(f"    {input_path} had no .png files.", file=sys.stderr)
        return

    # Adjust to respect the pivot.
    # We need to guarantee that the bounds have shrunk proportionately to the pivot aspect ratio.
    print("  Adjusting Pivot...")
    if pivot[X] < 1.0:
        pivot_ratio_x: float = pivot[X] / (1 - pivot[X])
        d_min_x: int = bb.min_x
        d_max_x: int = image.width - bb.max_x
        print("    pivot_ratio_x =", pivot_ratio_x)
        print("    d_min_x =", d_min_x)
        print("    d_max_x =", d_max_x)

        # If the min shrunk too much relative to the max
        if (d_min_x / d_max_x) > pivot_ratio_x:
            offset_x = int(d_min_x - d_max_x * pivot_ratio_x)
            bb.min_x -= offset_x
        else:
            offset_x = int(d_max_x - d_min_x / pivot_ratio_x)
            bb.max_x += offset_x

    if pivot[Y] < 1.0:
        pivot_ratio_y: float = pivot[Y] / (1 - pivot[Y])
        d_min_y: int = bb.min_y
        d_max_y: int = image.height - bb.max_y
        print("    pivot_ratio_y =", pivot_ratio_y)
        print("    d_min_y =", d_min_y)
        print("    d_max_y =", d_max_y)

        # If the min shrunk too much relative to the max
        if (d_min_y / d_max_y) > pivot_ratio_y:
            offset_y = int(d_min_y - d_max_y * pivot_ratio_y)
            bb.min_y -= offset_y
        else:
            offset_y = int(d_max_y - d_min_y / pivot_ratio_y)
            bb.max_y += offset_y

    bb.round_bounds(4)
    return bb


def crop_images(input_path: Path, pivot: Vec2, output_path: Path, root_path: Path):
    """Crop images in this path and save the output to output_path"""
    bb: Optional[BoundingBox] = getbbox(input_path, pivot)

    for infile in glob.glob(f"{input_path}/**/*.png", recursive=True):
        with Image.open(infile) as image:
            cropped_image: Image = bb.crop(image)
            output_file: Path = output_path / Path(infile).relative_to(root_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            print("  Writing to", output_file)
            cropped_image.save(output_file)


def main(root_dir: str, output_dir: str, inputs: List[Tuple[Vec2, List[str]]]):
    root_path: Path = Path(root_dir)
    output_path: Path = root_path / output_dir
    for pivot, paths in inputs:
        for input_dir in paths:
            input_path: Path = root_path / input_dir
            print("Processing images in ", input_path, "with pivot", pivot)
            crop_images(input_path, pivot, output_path, root_path)


if __name__ == "__main__":
    main(config.root_dir, config.output_dir, config.inputs)
