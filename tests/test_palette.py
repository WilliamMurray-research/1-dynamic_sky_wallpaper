import unittest
from PIL import Image
from renderer.palette import apply_palette

class TestPalette(unittest.TestCase):
    def test_day_palette(self):
        img = Image.new("RGBA", (100, 100), (100, 100, 100, 255))
        out = apply_palette(img, "day")
        self.assertEqual(out.size, img.size)
