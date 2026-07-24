import unittest
from PIL import Image
from renderer.tree import apply_tree_wind

class TestTree(unittest.TestCase):
    def test_tree_rotation(self):
        img = Image.new("RGBA", (300, 300))
        out = apply_tree_wind(img, "breeze")
        self.assertEqual(out.size, img.size)
