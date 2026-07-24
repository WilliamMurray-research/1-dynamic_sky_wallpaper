# Scene DSL Specification (v1.1)

## 1. Purpose  
The Scene DSL defines a **symbolic, deterministic description** of the environment used by the rendering pipeline.  
It compresses real‑world telemetry (sun, moon, weather, tide, wind) into a stable JSON structure that can be interpreted by any renderer — tiny model, shader, or procedural engine.

DSL v1.1 extends v1.0 with new fields for the **cartoon island** environment.

For deeper exploration:  
- scene DSL  
- rule engine  
- digital twin architecture

---

## 2. DSL Structure

A valid scene description is a JSON object containing:

```json
{
  "version": "1.1",

  "sunposition": "<enum>",
  "sun_height": "<enum>",
  "sky_mode": "<enum>",
  "weather": "<enum>",
  "moon": "<enum>",
  "stars": "<boolean>",

  "tide_state": "<enum>",
  "wind_strength": "<enum>",
  "wave_intensity": "<enum>",
  "island_palette": "<enum>"
}
```

All v1.0 fields remain required.  
All v1.1 fields are optional but recommended.

---

## 3. Field Definitions (v1.0 Fields)

### 3.1 `sunposition`
**Domain:** `"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`  
**Semantics:** Solar azimuth bucket.  
**Interpreter Contract:** Controls sun placement.

### 3.2 `sun_height`
**Domain:** `"none" | "low" | "medium" | "high"`  
**Semantics:** Solar altitude bucket.  
**Interpreter Contract:** Controls vertical placement + brightness.

### 3.3 `sky_mode`
**Domain:** `"night" | "dawn" | "day" | "dusk"`  
**Semantics:** Time‑of‑day category.  
**Interpreter Contract:** Controls gradient palette.

### 3.4 `weather`
**Domain:** `"clear" | "cloudy" | "approaching_rain" | "rain"`  
**Semantics:** Weather state.  
**Interpreter Contract:** Controls clouds + rain.

### 3.5 `moon`
**Domain:** `"none" | "crescent" | "half" | "gibbous" | "full"`  
**Semantics:** Visible lunar phase.  
**Interpreter Contract:** Controls moon rendering.

### 3.6 `stars`
**Domain:** `true | false`  
**Semantics:** Star visibility.  
**Interpreter Contract:** Controls starfield.

---

## 4. Field Definitions (v1.1 Extensions)

### 4.1 `tide_state`
Symbolic tide height.

**Domain:** `"low" | "medium" | "high"`  
**Semantics:** Derived from tide telemetry.  
**Interpreter Contract:** Controls waterline height.

---

### 4.2 `wind_strength`
Symbolic wind intensity.

**Domain:** `"none" | "breeze" | "windy" | "strong"`  
**Semantics:** Derived from wind speed.  
**Interpreter Contract:** Controls palm tree lean + motion cues.

---

### 4.3 `wave_intensity`
Symbolic ocean surface state.

**Domain:** `"calm" | "gentle" | "rough" | "storm"`  
**Semantics:** Derived from wind + weather.  
**Interpreter Contract:** Controls wave height + ocean texture.

---

### 4.4 `island_palette`
Symbolic colour theme for the island scene.

**Domain:** `"day" | "sunset" | "night"`  
**Semantics:** Derived from sky_mode.  
**Interpreter Contract:** Controls global palette.

---

## 5. Semantic Rules (Telemetry → DSL)

### 5.1 Sunposition  
- altitude < 0° → `"none"`  
- otherwise bucket azimuth into quadrants

### 5.2 Sun_height  
- alt < 0° → `"none"`  
- alt < 10° → `"low"`  
- alt < 35° → `"medium"`  
- alt ≥ 35° → `"high"`

### 5.3 Sky_mode  
- alt < −6° → `"night"`  
- −6° ≤ alt ≤ 6° → `"dawn"` or `"dusk"`  
- alt > 6° → `"day"`

### 5.4 Weather  
Derived from cloud cover + precipitation probability.

### 5.5 Moon  
- moon altitude < 0° → `"none"`  
- phase fraction < 0.1 → `"none"`  
- otherwise bucket phase

### 5.6 Stars  
`true` only when:  
- `sky_mode = "night"`  
- `moon = "none"`

---

## 6. Semantic Rules (v1.1 Extensions)

### 6.1 Tide → `tide_state`
- tide_height < 0.5 m → `"low"`  
- 0.5–1.2 m → `"medium"`  
- > 1.2 m → `"high"`

### 6.2 Wind → `wind_strength`
- speed < 2 m/s → `"none"`  
- 2–5 m/s → `"breeze"`  
- 5–10 m/s → `"windy"`  
- > 10 m/s → `"strong"`

### 6.3 Waves → `wave_intensity`
Derived from wind + weather:

- none/breeze + clear → `"calm"`  
- breeze/windy + cloudy → `"gentle"`  
- windy + approaching_rain → `"rough"`  
- strong + rain → `"storm"`

### 6.4 Palette → `island_palette`
- sky_mode = day → `"day"`  
- sky_mode = dawn/dusk → `"sunset"`  
- sky_mode = night → `"night"`

---

## 7. Versioning Rules

1. New fields must be optional.  
2. Existing fields must not change semantics.  
3. Renderers must ignore unknown fields gracefully.  
4. Breaking changes require a major version bump.  
5. Telemetry must remain raw; interpretation must remain symbolic.

---

## 8. Interpreter Contract

Any renderer must:

1. Accept a valid DSL JSON object.  
2. Treat all fields deterministically.  
3. Ignore unknown fields.  
4. Produce consistent output for identical DSL input.  
5. Fail gracefully on malformed input.

---

## 9. Summary  
DSL v1.1 extends the sky‑based digital twin into a **cartoon island environmental twin**, adding symbolic fields for tide, wind, waves, and palette.  
It remains deterministic, backward‑compatible, renderer‑agnostic, and easy to extend.

---

