from PIL import Image


# Deterministic lean angles (degrees)
LEAN_MAP = {
    "none":   0,
    "breeze": 3,
    "windy":  6,
    "strong": 10,
}


TREE_ASSET = "assets/tree.png"


def apply_tree_wind(img, wind_strength: str):
    """
    Deterministic palm‑tree wind transform.
    The tree sprite is rotated slightly based on wind_strength.
    """

    lean_deg = LEAN_MAP.get(wind_strength, 0)

    # Load tree sprite
    tree = Image.open(TREE_ASSET).convert("RGBA")

    # Rotate deterministically
    tree_rot = tree.rotate(-lean_deg, resample=Image.BICUBIC, expand=True)

    # Position tree at fixed anchor point
    w, h = img.size
    tw, th = tree_rot.size

    # Anchor: bottom‑left of island
    x = int(w * 0.12)
    y = int(h * 0.45) - th

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay.paste(tree_rot, (x, y), tree_rot)

    return Image.alpha_composite(img.convert("RGBA"), overlay)
