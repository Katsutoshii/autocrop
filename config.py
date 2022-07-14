"""Configure autocrop tool.
"""
from typing import List, Tuple

DirectoryGroups = List[List[str]]
Pivot = Tuple[float, float]

# Relative or absolute path to output cropped images.
output_dir: str = "../../Art/Animation/"

# Root directory combined with given input directories
root_dir: str = "../../Art/Animation_Ignore~/"

center = (0.5, 0.5)
left_bottom = (0, 1)
right_bottom = (1, 1)
right_top = (1, 0)
left = (0, 0.5)
right = (1, 0.5)
bottom = (0.5, 1)

person = (0.6, 0.75)

# Each config entry is of the form: (Pivot, Directory Groups)
# Each directory group is a list of paths that should share the same total bounding box.
# For example, if you want to crop with pivot (0.5, 0.5) in directories "A", "B", and "C",
# but only want "A" and "B" to share the same bounding box, use the following config:
# `(0.5, 0.5), [["A", "B"], ["C"]]`
inputs: List[Tuple[Pivot, DirectoryGroups]] = [
    (center, [
        # ["Flashback 2 MeetCute/B"],
        # ["Flashback 2 MeetCute/A2"],
        # ["Flashback 2 MeetCute/B2"],
        # ["Flashback 2 MeetCute/Eat Table"],
        # ["Flashback 2 MeetCute/Bg"],
        # ["Photos App"],

        # ["Good Epilogue/WFH/Desk"],
        # ["Good Epilogue/Therapy/AB"],
        # ["Good Epilogue/Therapy/Bg"],
        # ["Good Epilogue/Therapy/Fg"],
        # ["Good Epilogue/Therapy/Therapist"],
        # ["Good Epilogue/Cute Date/B"],
        # ["Good Epilogue/Cute Date/B_Bg"],
        # ["Good Epilogue/Cute Date/B_Fg"],
        # ["Good Epilogue/Cute Date/AWalk"],
        # ["Good Epilogue/Cute Date/BWalk"],
        # ["Good Epilogue/Cute Date/Zoom Out_AB"],
        # ["Good Epilogue/Cute Date/Zoom Out_Bg"],

        # ["Leave Epilogue/Leave/A"],
        # ["Leave Epilogue/Leave/B"],
        # ["Leave Epilogue/Bred"],
        # ["Leave Epilogue/Zone/Space"],
        # ["Leave Epilogue/Zone/A"],

        ["Flashback 3 Good Times/Dreams/AB"]
    ]),

    # (person, [
    #     ["Flashback 2 MeetCute/A"],
    # ]),

    (bottom, [
        # ["Flashback 2 MeetCute/FriendA"]

        # ["Good Epilogue/WFH/A"],
        # ["Good Epilogue/WFH/B"]
    ]),

    (left, [
        # ["Good Epilogue/Cute Date/A"]
    ]),
]

# If true, plot the pivot point on the image.
debug: bool = False
