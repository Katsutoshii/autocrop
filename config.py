"""Configure autocrop tool.
"""
from typing import List, Tuple

# Relative or absolute path to output cropped images.
output_dir: str = "output"

# Root directory combined with given input directories
root_dir: str = "testdata"

# Each config entry is of the form: (Pivot, Directories)
inputs: List[Tuple[Tuple[int, int], List[str]]] = [
    ((0.25, 0.5), ["Motion"]),
]

# If true, plot the pivot point on the image.
debug: bool = False
