import unittest
from telemetry.astronomy import compute_solar, compute_lunar

class TestAstronomy(unittest.TestCase):
    def test_solar_deterministic(self):
        s1 = compute_solar(-33.185, 138.017)
        s2 = compute_solar(-33.185, 138.017)
        self.assertAlmostEqual(s1.altitude, s2.altitude, places=6)
        self.assertAlmostEqual(s1.azimuth, s2.azimuth, places=6)

    def test_lunar_phase_range(self):
        m = compute_lunar(-33.185, 138.017)
        self.assertTrue(0 <= m.phase <= 1)
