import unittest
from pathlib import Path
from PIL import Image
from renderer.compositor import render_scene

class TestCompositor(unittest.TestCase):
    def test_render_scene(self):
        scene = {
            "island_palette": "day",
            "tide_state": "low",
            "wave_intensity": "calm",
            "wind_strength": "none",
            "sunposition": "topright",
            "sun_height": "high",
            "sky_mode": "day",
            "moon": "none",
            "stars": False,
            "weather": 0,
            "daily_state": "day_progress",
        }

        out = Path("tests/tmp_output.png")
        render_scene(scene, out)

        self.assertTrue(out.exists())
        img = Image.open(out)
        self.assertEqual(img.size[0] > 0, True)
