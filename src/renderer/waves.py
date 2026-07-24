from PIL import Image

# Deterministic wave overlays
ASSETS = {
    "calm":   "assets/waves_calm.png",
    "gentle": "assets/waves_gentle.png",
    "rough":  "assets/waves_rough.png",
    "storm":  "assets/waves_storm.png",
}


def apply_waves(img, wave_intensity: str):
    """
    Deterministic ocean texture overlay.
    wave_intensity is one of:
      calm | gentle | rough | storm
    """

    asset = ASSETS.get(wave_intensity)
    if not asset:
        return img  # fallback: no change

    overlay = Image.open(asset).convert("RGBA")

    # Composite overlay directly — deterministic
    return Image.alpha_composite(img.convert("RGBA"), overlay)
