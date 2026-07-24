import json
from pathlib import Path


DEFAULT_CONFIG_PATH = Path("config.json")


REQUIRED_FIELDS = {
    "location": ["lat", "lon"],
    "updateintervalminutes": None,
    "sleep_time": None,
    "work_start": None,
    "break_times": None,
    "wallpaper_output": None,
    "bom_location_id": None,
}


class ConfigError(Exception):
    pass


def load_config(path: Path = DEFAULT_CONFIG_PATH):
    """
    Load and validate config.json.
    Deterministic: same file → same config dict.
    """

    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    with open(path, "r") as f:
        cfg = json.load(f)

    validate_config(cfg)
    return cfg


def validate_config(cfg):
    """
    Ensures required fields exist and have correct structure.
    No symbolic interpretation.
    """

    for key, subkeys in REQUIRED_FIELDS.items():
        if key not in cfg:
            raise ConfigError(f"Missing required config field: {key}")

        if subkeys is None:
            # Simple scalar field
            continue

        # Nested fields
        if not isinstance(cfg[key], dict):
            raise ConfigError(f"Field '{key}' must be an object")

        for sk in subkeys:
            if sk not in cfg[key]:
                raise ConfigError(f"Missing required field: {key}.{sk}")

    # Basic type checks
    if not isinstance(cfg["break_times"], list):
        raise ConfigError("break_times must be a list of HH:MM strings")

    if not isinstance(cfg["updateintervalminutes"], int):
        raise ConfigError("updateintervalminutes must be an integer")

    if not isinstance(cfg["wallpaper_output"], str):
        raise ConfigError("wallpaper_output must be a string path")

    if not isinstance(cfg["bom_location_id"], str):
        raise ConfigError("bom_location_id must be a BOM location ID string")
