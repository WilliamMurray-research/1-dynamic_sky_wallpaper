import requests
import datetime


# ------------------------------------------------------------
# BOM Tide API Endpoint
# ------------------------------------------------------------

TIDES_URL = (
    "https://api.weather.bom.gov.au/v1/locations/{loc_id}/forecasts/tides"
)


# ------------------------------------------------------------
# Location → BOM Location ID
# ------------------------------------------------------------

def get_location_id(config):
    """
    The BOM API requires a location ID (e.g., 'IDS60901').
    The user must specify this in config.json.
    """
    return config["bom_location_id"]


# ------------------------------------------------------------
# Fetch Tide Forecasts
# ------------------------------------------------------------

def fetch_tides(loc_id):
    url = TIDES_URL.format(loc_id=loc_id)
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()


# ------------------------------------------------------------
# Parse ISO timestamp → datetime
# ------------------------------------------------------------

def parse_time(ts):
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))


# ------------------------------------------------------------
# Select Tide Height Closest to Now
# ------------------------------------------------------------

def select_current_tide_height(tides_json):
    """
    BOM returns:
      "tides": [
        { "height": 0.82, "time": "2026-07-24T21:00:00+09:30", "type": "high" },
        ...
      ]
    We pick the tide event whose time is closest to now.
    """

    try:
        tides = tides_json["tides"]
    except Exception:
        return 0.0  # fallback

    now = datetime.datetime.now(datetime.timezone.utc)

    closest = None
    closest_dt = None

    for t in tides:
        try:
            h = float(t["height"])
            dt = parse_time(t["time"])
        except Exception:
            continue

        if closest is None:
            closest = h
            closest_dt = dt
            continue

        if abs((dt - now).total_seconds()) < abs((closest_dt - now).total_seconds()):
            closest = h
            closest_dt = dt

    return closest if closest is not None else 0.0


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------

def fetch_tide_height(lat, lon, config=None):
    """
    Returns tide height in metres.
    lat/lon unused here — BOM requires location ID.
    """
    loc_id = get_location_id(config)
    tides_json = fetch_tides(loc_id)
    return select_current_tide_height(tides_json)
