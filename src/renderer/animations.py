from PIL import Image

# Deterministic daily‑state → asset mapping
ASSETS = {
    "morning_start": "assets/anim_morning_coffee.png",
    "work_start":    "assets/anim_work_sit.png",
    "day_progress":  None,  # no overlay
    "break_time":    "assets/anim_break_callisthenics.png",
    "evening":       "assets/anim_evening_wave.png",
    "sleep_time":    "assets/anim_sleep_campfire.png",
}


def apply_daily_animation(img, daily_state: str):
    """
    Deterministic daily‑rhythm animation overlay.
    Each state corresponds to a fixed sprite PNG.
    """

    asset = ASSETS.get(daily_state)
    if not asset:
        return img  # no overlay for this state

    overlay = Image.open(asset).convert("RGBA")

    # Position animation sprite at deterministic anchor
    w, h = img.size
    ow, oh = overlay.size

    # Anchor: bottom‑right of island
    x = int(w * 0.70)
    y = int(h * 0.55) - oh

    canvas = Image.new("RGBA", img.size, (0, 0, 0, 0))
    canvas.paste(overlay, (x, y), overlay)

    return Image.alpha_composite(img.convert("RGBA"), canvas)
