import unittest
from telemetry.bom_tide import select_current_tide_height
import datetime

class TestBOMTide(unittest.TestCase):
    def test_select_closest_tide(self):
        tides = {
            "tides": [
                {"height": 0.5, "time": "2026-07-24T10:00:00+00:00"},
                {"height": 1.2, "time": "2026-07-24T11:00:00+00:00"},
            ]
        }
        # Fake now = 10:30 UTC
        datetime.datetime.now = lambda tz=None: datetime.datetime(2026, 7, 24, 10, 30, tzinfo=datetime.timezone.utc)

        h = select_current_tide_height(tides)
        self.assertEqual(h, 0.5)
