import unittest
from PIL import Image
from renderer.animations import apply_daily_animation

class TestAnimations(unittest.TestCase):
    def test_no_overlay(self):
        img = Image.new("RGBA", (300, 300))
        out = apply_daily_animation(img, "day_progress")
        self.assertEqual(out.size, img.size)
