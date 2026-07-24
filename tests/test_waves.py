import unittest
from PIL import Image
from renderer.waves import apply_waves

class TestWaves(unittest.TestCase):
    def test_no_asset(self):
        img = Image.new("RGBA", (100, 100))
        out = apply_waves(img, "unknown")
        self.assertEqual(out.size, img.size)
