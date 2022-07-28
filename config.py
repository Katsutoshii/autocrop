"""Configure autocrop tool.
"""

# directions to self:
# 1. export main clip to Animation_Ignore~ folder
# 2. Export bus.clip to to Animation_Ignore~/Bus folder
# 3. Export photos.clip to Animation_Ignore~/Photos folder
# 4. run python3 ./main.py
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
personB = (0.4, 0.75)

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

    # (personB, [
    #     ["Flashback 2 MeetCute/A"],
    # ]),

    (bottom, [
        # ["Flashback 2 MeetCute/FriendA"]

        # ["Good Epilogue/WFH/A"],
        # ["Good Epilogue/WFH/B"]
    ]),

    # (left, [
    # ["Good Epilogue/Cute Date/A"]
    # Characters
    (person, [
        [
            "Motion/A",
            "Scene 2 Eating w Friends/IdleToSit",
            "Scene 3 Waiting for Bus/Getting up",
            "Scene 3 Waiting for Bus/Idle Bus",
            "Scene 4 Bus/Get Off Bus",
            "Scene 4 Bus/Get On Bus",
            "Scene 4 Bus/Sit On Bus",
            "Scene 5-6 To Condo/Run up Stairs",
            "Scene 5-6 To Condo/Walk up Stairs",
            "Scene 5-6 To Condo/Walk down Stairs",
            "Scene 7 Reunite Sad/SadA"
        ],
        ["Motion/B", ]
    ]),

    (right, [["Scene 1 Waking up/Wake up", ]]),

    # Scenery
    (center, [
        ["Scene 1 Waking up/Bed"],
        ["Scene 2 Eating w Friends/Bg", ],

        ["Bus/BusDoorLeft", ],
        ["Bus/BusDoorRight", ],
        ["Bus/BusInside", ],
        ["Bus/BusOutside", ],
        ["Bus/Scenery/Fg", ],
        ["Bus/Scenery/Mg", ],
        ["Bus/Scenery/Bg", ],

        ["Scene 5-6 To Condo/Stairs/Condo Stairs Down", ],
        ["Scene 5-6 To Condo/Stairs/Condo Stairs Up", ],
        ["Scene 5-6 To Condo/Condo Door", ],
        ["Scene 5-6 To Condo/Walk down Stairs Suitcase", ],
        ["Scene 7 Reunite Sad/Condo Bg Camera/CondoBg", ],
        ["Scene 7 Reunite Sad/Condo Bg Camera/CondoMg", ],
        ["Scene 7 Reunite Sad/Condo Fg Camera/CondoFg", ],
        ["Scene 7 Reunite Sad/Condo Fg Camera/CondoFg Suitcases", ],

        ["Scene 8 Reunite Happy/SadB"],

        ["Photos/Good", "Photos/Leave", ],

        ["Scene 2 Eating w Friends/Dish", ],
    ],),

    (right_top, [["Scene 7 Reunite Sad/SadB", ]]),

    # Finale
    (left, [["Scene 8 Reunite Happy/A Water"]]),
    (left_bottom, [
        ["Scene 2 Eating w Friends/Friend A", ],
        ["Scene 8 Reunite Happy/A_A"],
        ["Scene 8 Reunite Happy/A_B"],
        ["Scene 8 Reunite Happy/A_C"],
        ["Scene 8 Reunite Happy/A_D"],
        ["Scene 8 Reunite Happy/A_E"],
    ]),
    (bottom, [
        ["Scene 3 Waiting for Bus/Bus Stop", ],
        ["Scene 8 Reunite Happy/A_G"],
        ["Scene 8 Reunite Happy/B_A"]
    ]),
    (right_bottom, [
        ["Scene 2 Eating w Friends/Friend B", ],
        ["Scene 8 Reunite Happy/B_B"],
        ["Scene 8 Reunite Happy/B_C"],
        ["Scene 8 Reunite Happy/B_D"],
        ["Scene 8 Reunite Happy/B_G"]
    ]),
]

# If true, plot the pivot point on the image.
debug: bool = False
