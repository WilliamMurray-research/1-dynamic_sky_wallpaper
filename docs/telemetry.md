# Telemetry Specification

## 1. Purpose  
The telemetry layer provides **raw real‑world data** to the system.  
It does *not* interpret, bucket, or symbolise anything — that is the job of the scene rules.  
Telemetry must be:

- accurate  
- numeric or categorical  
- timestamped  
- free of DSL semantics  

This ensures the digital‑twin pipeline remains clean and modular.

---

## 2. Telemetry Sources  
The system currently supports three categories of telemetry:

1. **Solar and lunar data**  
2. **Weather data**  
3. **Optional tide data**

Each source is fetched independently and returned as raw values.

For deeper exploration:  
- sun/moon telemetry  
- weather telemetry  
- tide telemetry

---

## 3. Solar & Lunar Telemetry (`src/api/sun_moon.py`)

### 3.1 Required Outputs  
The module must return a dictionary containing:

```json
{
  "sun_alt": <float>,      // degrees
  "sun_az": <float>,       // degrees
  "moon_alt": <float>,     // degrees
  "moon_phase": <float>    // 0.0 = new, 1.0 = full
}
```

### 3.2 Semantics  
- `sun_alt` — solar altitude above/below horizon  
- `sun_az` — solar azimuth (0–360°)  
- `moon_alt` — lunar altitude  
- `moon_phase` — fractional illumination  

### 3.3 Source Options  
You may use:

- Open‑Meteo astronomy API  
- NOAA solar position API  
- PyEphem / Astral for local computation  

The implementation must be deterministic and return raw values only.

---

## 4. Weather Telemetry (`src/api/weather.py`)

### 4.1 Required Outputs  
The module must return:

```json
{
  "cloud_cover": <float>,        // percentage
  "precip_prob": <float>,        // percentage
  "precip_intensity": <float>,   // mm/hr
  "conditions": "<string>"       // provider-specific descriptor
}
```

### 4.2 Semantics  
- `cloud_cover` — total cloud fraction  
- `precip_prob` — probability of rain  
- `precip_intensity` — rain rate  
- `conditions` — raw descriptor (e.g., “light rain”, “clear”)  

### 4.3 Source Options  
Common providers:

- OpenWeather  
- WeatherAPI  
- Open‑Meteo  

The module must not convert weather into DSL categories — that is handled in `scene/rules.py`.

---

## 5. Tide Telemetry (`src/api/tides.py`) (Optional)

### 5.1 Required Outputs  
If enabled, return:

```json
{
  "tide_height": <float>,     // metres
  "tide_state": "<string>"    // raw descriptor
}
```

### 5.2 Semantics  
- `tide_height` — absolute water level  
- `tide_state` — provider descriptor (e.g., “rising”, “falling”)  

### 5.3 Source Options  
For Australia (user location: Port Pirie, SA):

- BOM tide endpoints  
- Local tide prediction libraries  

Tide data is optional and not required for core rendering.

---

## 6. Telemetry Update Cycle  
Telemetry is fetched at a fixed interval defined in `config.json`:

```json
"updateintervalminutes": 5
```

Rules:

1. All telemetry must be fetched fresh each cycle.  
2. Telemetry modules must not cache or reuse previous values.  
3. Failures must return `None` or raise a controlled exception.  
4. The main loop handles retries and fallback behaviour.

---

## 7. Error Handling  
Telemetry modules must:

- fail gracefully  
- return partial data if possible  
- never produce DSL values  
- never guess or infer missing values  

If a provider fails, the module should return:

```json
{
  "error": "<string>"
}
```

The scene builder decides how to handle missing fields.

---

## 8. Determinism Requirements  
Telemetry must be:

- timestamped  
- reproducible given the same timestamp and location  
- free of randomness  
- free of symbolic interpretation  

This ensures the DSL remains stable and predictable.

---

## 9. Telemetry → DSL Boundary  
Telemetry ends where interpretation begins.

Telemetry modules **must not**:

- bucket values  
- classify sky modes  
- determine sunposition  
- interpret moon phase  
- decide star visibility  
- generate prompts  

All symbolic logic belongs in:

- scene rules  
- DSL spec

Telemetry is raw input only.

---

## 10. Summary  
The telemetry layer provides raw, accurate, deterministic real‑world data to the system.  
It is intentionally simple and strictly separated from the DSL and rendering logic.  
This separation ensures the digital‑twin pipeline remains modular, testable, and extensible.

---

