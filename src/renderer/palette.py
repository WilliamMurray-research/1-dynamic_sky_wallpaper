from PIL import Image, ImageEnhance


def apply_palette(img: Image.Image, palette: str) -> Image.Image:
    """
    Deterministic palette recolouring.
    The base island image is recoloured using simple, stable transforms.
    """

    if palette == "day":
        return apply_day_palette(img)

    if palette == "sunset":
        return apply_sunset_palette(img)

    if palette == "night":
        return apply_night_palette(img)

    # Fallback: no change
    return img


# ------------------------------------------------------------
# Day Palette
# ------------------------------------------------------------

def apply_day_palette(img: Image.Image) -> Image.Image:
    """
    Bright, neutral colours.
    """
    # Slight brightness boost
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05)

    # Slight saturation boost
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.10)

    return img


# ------------------------------------------------------------
# Sunset Palette
# ------------------------------------------------------------

def apply_sunset_palette(img: Image.Image) -> Image.Image:
    """
    Warm, orange‑tinted palette.
    Deterministic overlay blend.
    """

    overlay = Image.new("RGBA", img.size, (255, 120, 60, 40))  # warm tint
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    # Slight contrast bump
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.08)

    return img


# ------------------------------------------------------------
# Night Palette
# ------------------------------------------------------------

def apply_night_palette(img: Image.Image) -> Image.Image:
    """
    Cool, darkened palette.
    Deterministic blue tint + brightness reduction.
    """

    # Blue tint overlay
    overlay = Image.new("RGBA", img.size, (40, 60, 160, 60))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)

    # Reduce brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.75)

    # Slight desaturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.85)

    return img
