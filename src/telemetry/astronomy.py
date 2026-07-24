import math
import datetime
from dataclasses import dataclass


@dataclass
class SolarResult:
    altitude: float
    azimuth: float


@dataclass
class LunarResult:
    altitude: float
    azimuth: float
    phase: float


# ------------------------------------------------------------
# Utility: Julian Date
# ------------------------------------------------------------

def julian_date(dt: datetime.datetime) -> float:
    """Compute Julian Date from a UTC datetime."""
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + dt.minute/60 + dt.second/3600) / 24

    if month <= 2:
        year -= 1
        month += 2

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)

    return (math.floor(365.25 * (year + 4716))
            + math.floor(30.6001 * (month + 1))
            + day + B - 1524.5)


# ------------------------------------------------------------
# Solar Position (NOAA simplified)
# ------------------------------------------------------------

def compute_solar(lat, lon):
    """
    Deterministic solar altitude + azimuth.
    lat, lon in degrees.
    """

    now = datetime.datetime.utcnow()
    jd = julian_date(now)
    n = jd - 2451545.0

    # Mean longitude
    L = (280.460 + 0.9856474 * n) % 360

    # Mean anomaly
    g = math.radians((357.528 + 0.9856003 * n) % 360)

    # Ecliptic longitude
    lam = math.radians(L + 1.915 * math.sin(g) + 0.020 * math.sin(2 * g))

    # Obliquity
    eps = math.radians(23.439 - 0.0000004 * n)

    # RA/Dec
    alpha = math.atan2(math.cos(eps) * math.sin(lam), math.cos(lam))
    delta = math.asin(math.sin(eps) * math.sin(lam))

    # Sidereal time
    GMST = (280.46061837 + 360.98564736629 * (jd - 2451545)) % 360
    LMST = math.radians(GMST + lon)

    # Hour angle
    H = LMST - alpha

    # Convert to altitude/azimuth
    lat_r = math.radians(lat)

    alt = math.asin(
        math.sin(lat_r) * math.sin(delta) +
        math.cos(lat_r) * math.cos(delta) * math.cos(H)
    )

    az = math.atan2(
        -math.sin(H),
        math.cos(lat_r) * math.tan(delta) - math.sin(lat_r) * math.cos(H)
    )

    # Convert to degrees
    alt_deg = math.degrees(alt)
    az_deg = (math.degrees(az) + 360) % 360

    return SolarResult(altitude=alt_deg, azimuth=az_deg)


# ------------------------------------------------------------
# Lunar Position (Simplified Meeus)
# ------------------------------------------------------------

def compute_lunar(lat, lon):
    """
    Deterministic lunar altitude + azimuth + phase.
    lat, lon in degrees.
    """

    now = datetime.datetime.utcnow()
    jd = julian_date(now)
    d = jd - 2451545.0

    # Mean longitude
    L = math.radians((218.316 + 13.176396 * d) % 360)

    # Mean anomaly
    M = math.radians((134.963 + 13.064993 * d) % 360)

    # Mean elongation
    D = math.radians((297.850 + 12.190749 * d) % 360)

    # Sun anomaly
    Ms = math.radians((357.529 + 0.9856003 * d) % 360)

    # Ecliptic longitude (approx)
    lam = L + math.radians(
        6.289 * math.sin(M)
        + 1.274 * math.sin(2 * D - M)
        + 0.658 * math.sin(2 * D)
        + 0.214 * math.sin(2 * M)
        - 0.186 * math.sin(Ms)
    )

    # Ecliptic latitude (approx)
    beta = math.radians(
        5.128 * math.sin(M)
        + 0.280 * math.sin(M + Ms)
        + 0.277 * math.sin(M - Ms)
        + 0.173 * math.sin(2 * D - M)
    )

    # Obliquity
    eps = math.radians(23.439 - 0.0000004 * d)

    # RA/Dec
    alpha = math.atan2(
        math.cos(eps) * math.sin(lam) - math.sin(eps) * math.sin(beta),
        math.cos(lam)
    )
    delta = math.asin(
        math.sin(eps) * math.sin(lam) * math.cos(beta) +
        math.cos(eps) * math.sin(beta)
    )

    # Sidereal time
    GMST = (280.46061837 + 360.98564736629 * (jd - 2451545)) % 360
    LMST = math.radians(GMST + lon)

    # Hour angle
    H = LMST - alpha

    lat_r = math.radians(lat)

    alt = math.asin(
        math.sin(lat_r) * math.sin(delta) +
        math.cos(lat_r) * math.cos(delta) * math.cos(H)
    )

    az = math.atan2(
        -math.sin(H),
        math.cos(lat_r) * math.tan(delta) - math.sin(lat_r) * math.cos(H)
    )

    alt_deg = math.degrees(alt)
    az_deg = (math.degrees(az) + 360) % 360

    # Phase (0 = new, 0.5 = full)
    phase = ((jd - 2451550.1) / 29.53058867) % 1

    return LunarResult(
        altitude=alt_deg,
        azimuth=az_deg,
        phase=phase
    )
