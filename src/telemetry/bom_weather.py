import requests
import math
from dataclasses import dataclass


# ------------------------------------------------------------
# BOM Weather API Endpoints
# ------------------------------------------------------------

OBSERVATIONS_URL = (
    "https://api.weather.bom.gov.au/v1/locations/{loc_id}/observations"
)

# ------------------------------------------------------------
# Weather Code Mapping (BOM → numeric)
# ------------------------------------------------------------

ICON_MAP = {
    "clear": 0,
    "mostly_sunny": 0,
    "partly_cloudy": 1,
    "cloudy": 1,
    "light_rain": 2,
    "rain": 2,
    "heavy_rain": 3,
    "storm": 4,
    "thunderstorm": 4,
}


# ------------------------------------------------------------
# Utility: km/h → m/s
# ------------------------------------------------------------

def kmh_to_ms(kmh):
    return kmh / 3.6


# ------------------------------------------------------------
# Location → BOM Location ID
# BOM requires a location ID, not lat/lon.
# For now, user provides location ID in config.json.
# ------------------------------------------------------------

def get_location_id(config):
    """
    The BOM API requires a location ID (e.g., 'IDS60901').
    The user must specify this in config.json.
    """
    return config["bom_location_id"]


# ------------------------------------------------------------
# Fetch Weather Observations
# ------------------------------------------------------------

def fetch_observations(loc_id):
    url = OBSERVATIONS_URL.format(loc_id=loc_id)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# ------------------------------------------------------------
# Extract Wind Speed (m/s)
# ------------------------------------------------------------

def extract_wind_speed(obs_json):
    """
    BOM returns:
      wind.speed_kilometre (km/h)
    We convert to m/s.
    """

    try:
        kmh = obs_json["data"]["wind"]["speed_kilometre"]
        return kmh_to_ms(kmh)
    except Exception:
        return 0.0  # fallback


# ------------------------------------------------------------
# Extract Weather Code (numeric)
# ------------------------------------------------------------

def extract_weather_code(obs_json):
    """
    BOM returns:
      icon_descriptor: "clear", "cloudy", "rain", etc.
    We map this to numeric weather_code.
    """

    try:
        icon = obs_json["data"]["icon_descriptor"]
        return ICON_MAP.get(icon, 1)  # default: cloudy
    except Exception:
        return 1


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def fetch_wind_speed(lat, lon, config=None):
    """
    Returns wind speed in m/s.
    lat/lon unused here — BOM requires location ID.
    """
    loc_id = get_location_id(config)
    obs = fetch_observations(loc_id)
    return extract_wind_speed(obs)


def fetch_weather_code(lat, lon, config=None):
    """
    Returns numeric weather_code.
    lat/lon unused here — BOM requires location ID.
    """
    loc_id = get_location_id(config)
    obs = fetch_observations(loc_id)
    return extract_weather_code(obs)
