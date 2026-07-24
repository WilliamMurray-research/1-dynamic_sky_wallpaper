import time
import json
import subprocess
from pathlib import Path

# --- Telemetry modules ---
from telemetry.astronomy import compute_solar, compute_lunar
from telemetry.bom_weather import fetch_weather_code, fetch_wind_speed
from telemetry.bom_tide import fetch_tide_height

# --- Renderer ---
from renderer.compositor import render_scene

# --- Wallpaper setter ---
from wallpaper.setter import set_wallpaper

# --- Config ---
from config.loader import load_config

# --- Prolog ---
from pyswip import Prolog


def prolog_emit_scene_json(prolog, telemetry):
    """
    Inject telemetry facts into Prolog, call emit_scene_json(JSON),
    and return the JSON scene as a Python dict.
    """

    # Clear previous facts
    prolog.assertz("retractall(sun_alt(_))")
    prolog.assertz("retractall(sun_az(_))")
    prolog.assertz("retractall(moon_alt(_))")
    prolog.assertz("retractall(moon_az(_))")
    prolog.assertz("retractall(moon_phase(_))")

    prolog.assertz("retractall(tide_height(_))")
    prolog.assertz("retractall(wind_speed(_))")
    prolog.assertz("retractall(weather_code(_))")

    prolog.assertz("retractall(current_time(_))")
    prolog.assertz("retractall(sleep_time(_))")
    prolog.assertz("retractall(work_start(_))")
    prolog.assertz("retractall(break_times(_))")

    # Inject telemetry facts
    prolog.assertz(f"sun_alt({telemetry['sun_alt']})")
    prolog.assertz(f"sun_az({telemetry['sun_az']})")

    prolog.assertz(f"moon_alt({telemetry['moon_alt']})")
    prolog.assertz(f"moon_az({telemetry['moon_az']})")
    prolog.assertz(f"moon_phase({telemetry['moon_phase']})")

    prolog.assertz(f"tide_height({telemetry['tide_height']})")
    prolog.assertz(f"wind_speed({telemetry['wind_speed']})")
    prolog.assertz(f"weather_code({telemetry['weather_code']})")

    prolog.assertz(f"current_time({telemetry['current_time']})")
    prolog.assertz(f"sleep_time({telemetry['sleep_time']})")
    prolog.assertz(f"work_start({telemetry['work_start']})")

    # Convert Python list → Prolog list
    breaks = telemetry["break_times"]
    breaks_list = "[" + ",".join(str(b) for b in breaks) + "]"
    prolog.assertz(f"break_times({breaks_list})")

    # Query Prolog
    result = list(prolog.query("emit_scene_json(JSON)"))[0]
    json_atom = result["JSON"]

    return json.loads(json_atom)


def gather_telemetry(config):
    """
    Collect all telemetry: astronomy + BOM.
    Returns a dict of raw numeric facts.
    """

    lat = config["location"]["lat"]
    lon = config["location"]["lon"]

    # Astronomy
    solar = compute_solar(lat, lon)
    lunar = compute_lunar(lat, lon)

    # BOM
    tide = fetch_tide_height(lat, lon)
    wind = fetch_wind_speed(lat, lon)
    weather = fetch_weather_code(lat, lon)

    # Daily rhythm times → seconds since midnight
    def to_seconds(tstr):
        h, m = map(int, tstr.split(":"))
        return h * 3600 + m * 60

    now = time.localtime()
    current_seconds = now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec

    return {
        "sun_alt": solar.altitude,
        "sun_az": solar.azimuth,

        "moon_alt": lunar.altitude,
        "moon_az": lunar.azimuth,
        "moon_phase": lunar.phase,

        "tide_height": tide,
        "wind_speed": wind,
        "weather_code": weather,

        "current_time": current_seconds,
        "sleep_time": to_seconds(config["sleep_time"]),
        "work_start": to_seconds(config["work_start"]),
        "break_times": [to_seconds(t) for t in config["break_times"]],
    }


def main():
    config = load_config()
    output_path = Path(config["wallpaper_output"])

    # Initialise Prolog
    prolog = Prolog()
    prolog.consult("src/prolog/rules.pl")
    prolog.consult("src/prolog/emit_json.pl")

    print("Dynamic Island Wallpaper — starting loop")

    while True:
        print("Gathering telemetry...")
        telemetry = gather_telemetry(config)

        print("Generating scene DSL...")
        scene = prolog_emit_scene_json(prolog, telemetry)

        print("Rendering wallpaper...")
        render_scene(scene, output_path)

        print("Applying wallpaper...")
        set_wallpaper(output_path)

        print("Sleeping...")
        time.sleep(config["updateintervalminutes"] * 60)


if __name__ == "__main__":
    main()
