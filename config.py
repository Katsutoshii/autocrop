"""Configure autocrop tool.
"""
from typing import List, Tuple
from autocrop import Pivot, DirectoryGroups


# Relative or absolute path to output cropped images.
output_dir: str = "output"

# Root directory combined with given input directories
root_dir: str = "testdata"

center = (0.5, 0.5)
left_bottom = (0, 1)
right_bottom = (1, 1)
right_top = (1, 0)
left = (0, 0.5)
right = (1, 0.5)
bottom = (0.5, 1)

person = (0.5, 0.75)

# Each config entry is of the form: (Pivot, Directory Groups)
# Each directory group is a list of paths that should share the same total bounding box.
# For example, if you want to crop with pivot (0.5, 0.5) in directories "A", "B", and "C",
# but only want "A" and "B" to share the same bounding box, use the following config:
# `(0.5, 0.5), [["A", "B"], ["C"]]`
inputs: List[Tuple[Pivot, DirectoryGroups]] = [
    ((0.5, 1), [["Motion"]]),
]

# If true, plot the pivot point on the image.
debug: bool = False
