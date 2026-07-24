# Telemetry  
Telemetry is the **first stage** of the Dynamic Island Wallpaper pipeline.  
It gathers **raw environmental and astronomical data**, converts nothing to symbolic form, and passes the raw values directly to the Prolog semantic engine.

Telemetry itself is **deterministic**:

> Given the same time, location, and BOM API responses → telemetry produces the same numeric facts.

Symbolic interpretation happens **only in Prolog**, never in telemetry.

---

## 1. Purpose  
Telemetry provides the Prolog engine with:

- solar position  
- lunar position  
- lunar phase  
- tide height (BOM)  
- wind speed (BOM)  
- weather state (BOM)  

These values are **raw numeric measurements**, not DSL categories.

Prolog is responsible for bucketing them into symbolic DSL fields.

---

## 2. Telemetry Sources  
Telemetry comes from two independent sources:

1. **Local astronomical computation**  
2. **Bureau of Meteorology (BOM) API**

This separation ensures clarity, testability, and deterministic behaviour.

---

# 3. Local Astronomy (Fully Deterministic)  
Astronomical values are computed locally using standard formulas.

### 3.1 Solar Position  
Computed values:

- **solar altitude** (degrees above/below horizon)  
- **solar azimuth** (compass direction)  

Derived from:

- observer latitude  
- observer longitude  
- Julian date  
- solar declination  
- hour angle  

### 3.2 Lunar Position  
Computed values:

- **lunar altitude**  
- **lunar azimuth**  
- **lunar phase fraction** (0–1)

### 3.3 Sunrise/Sunset  
Computed using solar altitude thresholds.

### 3.4 Output  
Astronomy produces raw numeric facts:

```
sun_alt(AltDegrees).
sun_az(AzimuthDegrees).
moon_alt(AltDegrees).
moon_az(AzimuthDegrees).
moon_phase(PhaseFraction).
sunrise(Time).
sunset(Time).
```

---

# 4. BOM API (External Environmental Telemetry)  
Environmental data is fetched from the **Bureau of Meteorology (BOM)**.  
This section documents the exact endpoints and how their fields map into your numeric telemetry facts.

---

## 4.1 BOM Endpoints Used

### **A. Weather Observations (Wind + Weather Code)**  
Endpoint (JSON):

```
https://api.weather.bom.gov.au/v1/locations/<location-id>/observations
```

This returns a structure containing:

- `wind.speed_kilometre`  
- `wind.gust_kilometre`  
- `wind.direction`  
- `cloud`  
- `rain_since_9am`  
- `weather` (text description)  
- `icon_descriptor` (symbolic weather code)  

### **B. Marine / Tide Predictions**  
Endpoint (JSON):

```
https://api.weather.bom.gov.au/v1/locations/<location-id>/forecasts/tides
```

This returns:

- `tides[].height` (metres)  
- `tides[].time` (ISO timestamp)  
- `tides[].type` (high/low)  

Telemetry selects the tide height closest to the current timestamp.

---

# 4.2 Mapping BOM → Telemetry Facts

## A. Tide Height Mapping  
From the tide endpoint:

```json
{
  "tides": [
    { "height": 0.82, "time": "2026-07-24T21:00:00+09:30", "type": "high" },
    ...
  ]
}
```

Telemetry selects the tide event closest to the current time:

```
tide_height(0.82).
```

No symbolic bucketing occurs here.

---

## B. Wind Speed Mapping  
From the observations endpoint:

```json
{
  "wind": {
    "speed_kilometre": 15.0,
    "gust_kilometre": 22.0,
    "direction": "NW"
  }
}
```

Telemetry converts km/h → m/s:

\[
\text{m/s} = \frac{\text{km/h}}{3.6}
\]

Example:

```
wind_speed(4.16).
```

Wind direction is ignored at the telemetry stage.

---

## C. Weather Code Mapping  
BOM provides a symbolic descriptor:

```json
{
  "icon_descriptor": "rain",
  "weather": "Showers increasing"
}
```

Telemetry maps `icon_descriptor` to a **numeric weather_code**:

| BOM `icon_descriptor` | weather_code |
|------------------------|--------------|
| `"clear"`              | 0 |
| `"mostly_sunny"`       | 0 |
| `"partly_cloudy"`      | 1 |
| `"cloudy"`             | 1 |
| `"light_rain"`         | 2 |
| `"rain"`               | 2 |
| `"heavy_rain"`         | 3 |
| `"storm"`              | 4 |
| `"thunderstorm"`       | 4 |

Example:

```
weather_code(2).
```

Prolog later converts this numeric code into symbolic DSL categories:

- `clear`  
- `cloudy`  
- `approaching_rain`  
- `rain`

Telemetry does **not** perform this symbolic mapping.

---

# 4.3 Output  
Environmental telemetry produces raw numeric facts:

```
tide_height(HeightMetres).
wind_speed(MetresPerSecond).
weather_code(Code).
```

These values are passed directly to Prolog.

---

# 5. Telemetry → Prolog Interface  
Telemetry never produces symbolic DSL fields.  
It only produces numeric facts.

Example full telemetry set:

```
sun_alt(12.4).
sun_az(145.0).
moon_alt(-5.0).
moon_az(210.0).
moon_phase(0.62).

tide_height(0.8).
wind_speed(4.2).
weather_code(2).

sunrise(07:12).
sunset(17:46).
```

Prolog receives these facts and applies semantic rules to produce the DSL.

---

# 6. Determinism  
Telemetry is deterministic **as long as BOM returns consistent data**.

- Local astronomy is strictly deterministic  
- BOM API responses are treated as deterministic inputs  
- Telemetry does not introduce randomness  
- Telemetry does not perform symbolic bucketing  
- Telemetry does not perform rendering logic  

Determinism is broken **only** if the renderer uses a generative transformation.

Telemetry remains deterministic regardless of renderer mode.

---

# 7. Error Handling  
If BOM data is unavailable:

- telemetry falls back to the last known values  
- Prolog receives fallback numeric facts  
- the DSL remains valid  
- the renderer continues to operate  

Astronomy is unaffected by BOM outages.

---

# 8. Summary  
Telemetry provides:

- **local deterministic astronomy**  
- **BOM environmental data**  
- **explicit endpoint mappings**  
- **raw numeric facts**  
- **no symbolic interpretation**  
- **no rendering instructions**  
- **no nondeterminism**

It is the foundation of the digital twin.

---

