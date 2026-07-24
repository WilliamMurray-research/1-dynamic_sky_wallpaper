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
- tide height  
- wind speed  
- weather state  

These values are **raw numeric measurements**, not DSL categories.

Prolog is responsible for bucketing them into symbolic DSL fields.

---

## 2. Telemetry Sources  
Telemetry comes from two independent sources:

1. **Local astronomical computation**  
2. **Bureau of Meteorology (BOM) API**

This separation ensures clarity, testability, and deterministic behaviour.

---

## 3. Local Astronomy (Fully Deterministic)  
Astronomical values are computed locally using standard formulas.

### 3.1 Solar Position  
Computed values:

- **solar altitude** (degrees above/below horizon)  
- **solar azimuth** (compass direction)  

These are derived from:

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
Computed using solar altitude thresholds:

- sunrise ≈ altitude crosses 0° upward  
- sunset ≈ altitude crosses 0° downward  

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

These values are passed directly to Prolog.

---

## 4. BOM API (External Environmental Telemetry)  
Environmental data is fetched from the **Bureau of Meteorology (BOM)**.

### 4.1 Tide Height  
BOM tide endpoints provide:

- predicted tide height (metres)  
- timestamped tide events  

Telemetry extracts the current tide height and passes it as a numeric value.

### 4.2 Wind Speed  
BOM weather observations provide:

- wind speed (m/s or km/h)  
- wind gusts  
- wind direction  

Telemetry normalises wind speed into m/s.

### 4.3 Weather State  
BOM provides:

- weather condition codes  
- cloud cover  
- precipitation  
- storm indicators  

Telemetry maps BOM’s condition codes into a **numeric weather_code**, not symbolic categories.

### 4.4 Output  
Environmental telemetry produces raw numeric facts:

```
tide_height(HeightMetres).
wind_speed(MetresPerSecond).
weather_code(Code).
```

These values are passed directly to Prolog.

---

## 5. Telemetry → Prolog Interface  
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

## 6. Determinism  
Telemetry is deterministic **as long as BOM returns consistent data**.

- Local astronomy is strictly deterministic  
- BOM API responses are treated as deterministic inputs  
- Telemetry does not introduce randomness  
- Telemetry does not perform symbolic bucketing  
- Telemetry does not perform rendering logic  

Determinism is broken **only** if the renderer uses a generative transformation.

Telemetry remains deterministic regardless of renderer mode.

---

## 7. Error Handling  
If BOM data is unavailable:

- telemetry falls back to the last known values  
- Prolog receives fallback numeric facts  
- the DSL remains valid  
- the renderer continues to operate  

Astronomy is unaffected by BOM outages.

---

## 8. Summary  
Telemetry provides:

- **local deterministic astronomy**  
- **BOM environmental data**  
- **raw numeric facts**  
- **no symbolic interpretation**  
- **no rendering instructions**  
- **no nondeterminism**

It is the foundation of the digital twin.

---

