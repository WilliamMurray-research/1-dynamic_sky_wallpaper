import unittest
from pyswip import Prolog

class TestRules(unittest.TestCase):
    def setUp(self):
        self.prolog = Prolog()
        self.prolog.consult("src/prolog/rules.pl")

    def test_sun_height_bucket(self):
        self.prolog.assertz("sun_alt(45)")
        self.prolog.assertz("sun_az(100)")
        self.prolog.assertz("moon_alt(-10)")
        self.prolog.assertz("moon_phase(0.5)")
        self.prolog.assertz("tide_height(0.5)")
        self.prolog.assertz("wind_speed(3)")
        self.prolog.assertz("weather_code(1)")
        self.prolog.assertz("current_time(36000)")
        self.prolog.assertz("sleep_time(82800)")
        self.prolog.assertz("work_start(32400)")
        self.prolog.assertz("break_times([39600])")

        result = list(self.prolog.query("scene(S)"))[0]["S"]
        self.assertEqual(result["sun_height"], "high")

    def test_tide_bucket(self):
        self.prolog.assertz("tide_height(0.2)")
        self.prolog.assertz("wind_speed(0)")
        self.prolog.assertz("weather_code(0)")
        self.prolog.assertz("sun_alt(-10)")
        self.prolog.assertz("sun_az(0)")
        self.prolog.assertz("moon_alt(-10)")
        self.prolog.assertz("moon_phase(0.1)")
        self.prolog.assertz("current_time(0)")
        self.prolog.assertz("sleep_time(82800)")
        self.prolog.assertz("work_start(32400)")
        self.prolog.assertz("break_times([])")

        result = list(self.prolog.query("scene(S)"))[0]["S"]
        self.assertEqual(result["tide_state"], "low")
