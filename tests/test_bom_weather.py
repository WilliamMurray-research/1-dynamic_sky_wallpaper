import unittest
from telemetry.bom_weather import extract_weather_code, extract_wind_speed

class TestBOMWeather(unittest.TestCase):
    def test_weather_code_mapping(self):
        obs = {"data": {"icon_descriptor": "rain"}}
        self.assertEqual(extract_weather_code(obs), 2)

    def test_wind_speed_conversion(self):
        obs = {"data": {"wind": {"speed_kilometre": 36}}}
        self.assertAlmostEqual(extract_wind_speed(obs), 10.0)
