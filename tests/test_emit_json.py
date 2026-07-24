import unittest
from pyswip import Prolog
import json

class TestEmitJSON(unittest.TestCase):
    def setUp(self):
        self.prolog = Prolog()
        self.prolog.consult("src/prolog/rules.pl")
        self.prolog.consult("src/prolog/emit_json.pl")

    def test_json_output(self):
        self.prolog.assertz("sun_alt(10)")
        self.prolog.assertz("sun_az(100)")
        self.prolog.assertz("moon_alt(0)")
        self.prolog.assertz("moon_phase(0.5)")
        self.prolog.assertz("tide_height(1.0)")
        self.prolog.assertz("wind_speed(4)")
        self.prolog.assertz("weather_code(2)")
        self.prolog.assertz("current_time(36000)")
        self.prolog.assertz("sleep_time(82800)")
        self.prolog.assertz("work_start(32400)")
        self.prolog.assertz("break_times([])")

        result = list(self.prolog.query("emit_scene_json(JSON)"))[0]["JSON"]
        scene = json.loads(result)

        self.assertIn("sunposition", scene)
        self.assertEqual(scene["version"], "0.0.1")
