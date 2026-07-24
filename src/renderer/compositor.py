from pathlib import Path
from PIL import Image, ImageEnhance

from .palette import apply_palette
from .waves import apply_waves
from .tree import apply_tree_wind
from .animations import apply_daily_animation


BASE_IMAGE_PATH = Path("assets/base_island.png")


def render_scene(scene, output_path: Path):
    """
    Deterministic compositor:
    - loads base island image
    - applies overlays based on DSL fields
    - writes final PNG to output_path
    """

    # Load base image
    base = Image.open(BASE_IMAGE_PATH).convert("RGBA")

    # 1. Palette (day/sunset/night)
    base = apply_palette(base, scene["island_palette"])

    # 2. Tide → shoreline mask
    base = apply_tide(base, scene["tide_state"])

    # 3. Waves → ocean texture
    base = apply_waves(base, scene["wave_intensity"])

    # 4. Tree → wind transform
    base = apply_tree_wind(base, scene["wind_strength"])

    # 5. Sky objects → sun/moon/stars
    base = apply_sky_objects(
        base,
        sunposition=scene["sunposition"],
        sun_height=scene["sun_height"],
        sky_mode=scene["sky_mode"],
        moon=scene["moon"],
        stars=scene["stars"],
        weather=scene["weather"],
    )

    # 6. Daily rhythm animation
    base = apply_daily_animation(base, scene["daily_state"])

    # Save final image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    base.save(output_path, format="PNG")


def apply_tide(img: Image.Image, tide_state: str) -> Image.Image:
    """
    Adjust waterline mask based on tide_state.
    Implementation detail: use precomputed masks or simple vertical crop.
    """
    # Example: darken or lighten lower band to simulate shoreline shift
    w, h = img.size
    band_height = int(h * 0.15)

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    band = Image.new("RGBA", (w, band_height), (0, 0, 0, 60))

    if tide_state == "low":
        y = int(h * 0.65)
    elif tide_state == "medium":
        y = int(h * 0.70)
    else:  # high
        y = int(h * 0.75)

    overlay.paste(band, (0, y))
    return Image.alpha_composite(img, overlay)


def apply_sky_objects(
    img: Image.Image,
    sunposition: str,
    sun_height: str,
    sky_mode: str,
    moon: str,
    stars: bool,
    weather,
) -> Image.Image:
    """
    Composite sun, moon, stars, and weather overlays.
    All assets are deterministic sprite PNGs.
    """

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    w, h = img.size

    # Sun
    if sunposition != "none" and sky_mode in ("dawn", "day", "dusk"):
        sun = Image.open("assets/sun.png").convert("RGBA")
        x, y = sun_coordinates(sunposition, sun_height, w, h)
        overlay.paste(sun, (x, y), sun)

    # Moon
    if moon != "none" and sky_mode in ("dusk", "night"):
        moon_img = Image.open(f"assets/moon_{moon}.png").convert("RGBA")
        overlay.paste(moon_img, (int(w * 0.75), int(h * 0.15)), moon_img)

    # Stars
    if stars and sky_mode == "night":
        stars_img = Image.open("assets/stars.png").convert("RGBA")
        overlay.paste(stars_img, (0, 0), stars_img)

    # Weather (clouds/rain)
    weather_overlay = weather_to_asset(weather)
    if weather_overlay:
        clouds = Image.open(weather_overlay).convert("RGBA")
        overlay.paste(clouds, (0, 0), clouds)

    return Image.alpha_composite(img, overlay)


def sun_coordinates(sunposition: str, sun_height: str, w: int, h: int):
    """
    Map symbolic sunposition + sun_height to pixel coordinates.
    Deterministic grid mapping.
    """
    # Horizontal
    if "left" in sunposition:
        x = int(w * 0.15)
    else:
        x = int(w * 0.75)

    # Vertical
    if sun_height == "low":
        y = int(h * 0.55)
    elif sun_height == "medium":
        y = int(h * 0.35)
    else:  # high
        y = int(h * 0.15)

    return x, y


def weather_to_asset(weather_code):
    """
    Map numeric weather_code to asset path.
    0: clear, 1: cloudy, 2: rain, 3: heavy rain, 4: storm
    """
    if weather_code in (0,):
        return None
    if weather_code in (1,):
        return "assets/clouds.png"
    if weather_code in (2, 3):
        return "assets/rain.png"
    if weather_code == 4:
        return "assets/storm.png"
    return None
