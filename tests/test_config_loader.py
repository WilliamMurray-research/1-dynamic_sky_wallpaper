import unittest
from config.loader import validate_config, ConfigError

class TestConfigLoader(unittest.TestCase):
    def test_missing_field(self):
        cfg = {
            "location": {"lat": 1, "lon": 2},
            "updateintervalminutes": 5,
            "sleep_time": "23:00",
            "work_start": "09:00",
            "break_times": [],
            "wallpaper_output": "out.png",
            # missing bom_location_id
        }
        with self.assertRaises(ConfigError):
            validate_config(cfg)
