"""Autocrop library.

Supporting utils for cropping images with a shared pivot point. 
"""
from typing import Optional, Tuple, List
import glob
from dataclasses import dataclass
import math
from pathlib import Path
from PIL import Image
import numpy as np
import sys
from copy import copy


X: int = 0
Y: int = 1


DirectoryGroups = List[List[str]]
Pivot = Tuple[float, float]


Int2 = Tuple[int, int]
Int4 = Tuple[int, int, int, int]


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    @staticmethod
    def from_image(image: Image, invert: bool = False) -> Optional["BoundingBox"]:
        """Constructs a bounding box from an image."""
        # `getbbox` only trims the black border. Thus we must
        # first replace white border before computing the
        # bounding box.
        data = np.array(image)
        red, green, blue, alpha = data.T
        white_areas = (red == 255) & (blue == 255) & (
            green == 255) & (alpha == 0)
        # replace (255,255,255,0) with (0,0,0,0)
        data[..., :-1][white_areas.T] = (0, 0, 0)
        image = Image.fromarray(data)

        img_result = image.getbbox()
        if img_result is None:
            print(BColors.WARNING +
                  "WARNING: Image is empty! Ignoring." + BColors.ENDC)
            return None
        min_x, min_y, max_x, max_y = img_result
        return BoundingBox(min_x, min_y, max_x, max_y)

    def grow_to_fit(self, other: "BoundingBox"):
        """Grow this bounding box to fit another."""
        self.min_x = min(other.min_x, self.min_x)
        self.min_y = min(other.min_y, self.min_y)
        self.max_x = max(other.max_x, self.max_x)
        self.max_y = max(other.max_y, self.max_y)

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


def get_bboxes(root_path: Path, input_dirs: List[str]) -> List[Optional[BoundingBox]]:
    """Loads image boundting boxes from the directory."""
    bbs: List[Optional[BoundingBox]] = []

    for input_dir in input_dirs:
        input_path: Path = root_path / input_dir
        for infile in glob.glob(f"{input_path}/**/*.png", recursive=True):
            with Image.open(infile) as image:
                bbs.append(BoundingBox.from_image(image))

    return bbs


def draw_square(image: Image, center: Int2, radius: int, color: Int4 = (255, 64, 64, 255)):
    """Draw a square at the given point. Used for debugging."""
    for i in range(radius * 2):
        for j in range(radius * 2):
            x: int = center[X] + i - radius
            y: int = center[Y] + j - radius
            if x >= 0 and x < image.width and y >= 0 and y < image.height:
                image.putpixel((x, y), color)


def get_total_bbox(bbs: List[Optional[BoundingBox]]) -> Optional[BoundingBox]:
    """Get the bounding box that covers all images in a directory and overwrites with a cropped version."""
    total_bb: Optional[BoundingBox] = None
    for bb in bbs:
        if bb is not None:
            if total_bb is None:
                total_bb = copy(bb)
            else:
                total_bb.grow_to_fit(bb)

    total_bb.round_bounds(4)
    return total_bb


def get_adjusted_bbox(bb: BoundingBox, total_bb: BoundingBox, pivot: Pivot) -> BoundingBox:
    """Given a bounding box `bb` that is contained within `total_bb`,
    Return `bb` shrunk as much as possible while keeping `pivot` at the same relative location.
    """
    adjusted_bb: BoundingBox = copy(bb)

    print(f"  Adjusting Pivot with {adjusted_bb}...")
    if pivot[X] == 0.0:
        adjusted_bb.min_x = total_bb.min_x
    elif pivot[X] == 1.0:
        adjusted_bb.max_x = total_bb.max_x
    else:
        pivot_ratio_x: float = pivot[X] / (1 - pivot[X])
        d_min_x: int = bb.min_x - total_bb.min_x
        d_max_x: int = total_bb.max_x - bb.max_x

        # If the min shrunk too much relative to the max
        if d_max_x == 0 or (d_min_x / d_max_x) > pivot_ratio_x:
            offset_x = int(d_min_x - d_max_x * pivot_ratio_x)
            adjusted_bb.min_x -= offset_x
        else:
            offset_x = int(d_max_x - d_min_x / pivot_ratio_x)
            adjusted_bb.max_x += offset_x

    if pivot[Y] == 0.0:
        adjusted_bb.min_y = total_bb.min_y
    elif pivot[Y] == 1.0:
        adjusted_bb.max_y = total_bb.max_y
    else:
        pivot_ratio_y: float = pivot[Y] / (1 - pivot[Y])
        d_min_y: int = bb.min_y - total_bb.min_y
        d_max_y: int = total_bb.max_y - bb.max_y

        # If the min shrunk too much relative to the max
        if d_max_y == 0 or (d_min_y / d_max_y) > pivot_ratio_y:
            offset_y = int(d_min_y - d_max_y * pivot_ratio_y)
            adjusted_bb.min_y -= offset_y
        else:
            offset_y = int(d_max_y - d_min_y / pivot_ratio_y)
            adjusted_bb.max_y += offset_y

    adjusted_bb.round_bounds(4)
    return adjusted_bb


def crop_images(root_path: Path, input_dirs: List[str], pivot: Pivot, output_path: Path, debug: bool = False):
    """Crop images in this path and save the output to output_path"""
    print("Processing images in the following directories:", input_dirs)
    print("Using pivot", pivot)

    bbs: List[Optional[BoundingBox]] = get_bboxes(root_path, input_dirs)
    if len(bbs) == 0:
        print(f"    Input directories had no .png files.", file=sys.stderr)
        return

    total_bb: Optional[BoundingBox] = get_total_bbox(bbs)

    for input_dir in input_dirs:
        input_path: Path = root_path / input_dir
        for i, infile in enumerate(glob.glob(f"{input_path}/**/*.png", recursive=True)):
            with Image.open(infile) as image:
                bb = BoundingBox.from_image(image)

                if bb is None:
                    continue

                adjusted_bb: BoundingBox = get_adjusted_bbox(
                    bb, total_bb, pivot)
                print("  Adjusted bb to", adjusted_bb)
                cropped_image: Image = adjusted_bb.crop(image)

                if debug:
                    pivot_x = int(cropped_image.width *
                                  pivot[X])
                    pivot_y = int(cropped_image.height * pivot[Y])
                    draw_square(cropped_image, (pivot_x, pivot_y), radius=4)

                output_file: Path = output_path / \
                    Path(infile).relative_to(root_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)

                print("  Writing to", output_file)
                cropped_image.save(output_file)
