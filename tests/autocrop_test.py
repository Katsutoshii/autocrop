"""
Basic unit tests for autocrop.
"""
from pathlib import Path

from autocrop import crop_images


def test_crop_images():
    """
    Test crop images
    """
    crop_images(Path("testdata"), ["Motion/A"], (0.5, 1), Path("output"))
    assert Path("output/Motion/A/Walk/Walk2a.png").exists()
    assert Path("output/Motion/A/Walk/Walk3.png").exists()
    assert Path("output/Motion/A/Walk/Walk3a.png").exists()
