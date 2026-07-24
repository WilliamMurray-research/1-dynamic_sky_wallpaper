# Scene DSL Specification (v1.0)

## 1. Purpose  
The Scene DSL defines a **symbolic description of the sky** used by the rendering pipeline.  
It compresses real‑world telemetry (sun, moon, weather, time) into a deterministic, interpretable JSON structure.  
The DSL is stable, versioned, and designed for forward‑compatible extension.

---

## 2. Document Structure  
A valid scene description is a JSON object containing the following required fields:

```json
{
  "version": "1.0",
  "sunposition": "<enum>",
  "sun_height": "<enum>",
  "sky_mode": "<enum>",
  "weather": "<enum>",
  "moon": "<enum>",
  "stars": "<boolean>"
}
```

Each field has a defined domain and semantics.

---

## 3. Field Definitions

### 3.1 `sunposition`
**Domain:**  
`"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`

**Semantics:**  
Symbolic quadrant derived from solar azimuth.

**Interpreter contract:**  
Renderer places the sun in the specified region.

---

### 3.2 `sun_height`
**Domain:**  
`"none" | "low" | "medium" | "high"`

**Semantics:**  
Bucketed solar altitude.

**Interpreter contract:**  
Controls vertical placement, brightness, and size.

---

### 3.3 `sky_mode`
**Domain:**  
`"night" | "dawn" | "day" | "dusk"`

**Semantics:**  
Colour gradient mode based on solar altitude and time.

**Interpreter contract:**  
Selects gradient palette.

---

### 3.4 `weather`
**Domain:**  
`"clear" | "cloudy" | "approaching_rain" | "rain"`

**Semantics:**  
Weather visual state derived from cloud cover and precipitation probability.

**Interpreter contract:**  
Controls cloud density, horizon darkness, and rain streaks.

---

### 3.5 `moon`
**Domain:**  
`"none" | "crescent" | "half" | "gibbous" | "full"`

**Semantics:**  
Visible lunar phase, derived from moon altitude and phase fraction.

**Interpreter contract:**  
Renderer draws correct moon shape or omits it.

---

### 3.6 `stars`
**Domain:**  
`true | false`

**Semantics:**  
Starfield visibility.

**Interpreter contract:**  
Renderer adds stars only when `true`.

---

## 4. Semantic Rules (Telemetry → DSL)

### 4.1 Sunposition  
- altitude < 0 → `"none"`  
- otherwise map azimuth to quadrant

### 4.2 Sun_height  
- alt < 0° → `"none"`  
- alt < 10° → `"low"`  
- alt < 35° → `"medium"`  
- alt ≥ 35° → `"high"`

### 4.3 Sky_mode  
- alt < −6° → `"night"`  
- −6° ≤ alt ≤ 6° → `"dawn"` or `"dusk"`  
- alt > 6° → `"day"`

### 4.4 Weather  
Derived from cloud cover, precipitation probability, and optionally wind.

### 4.5 Moon  
- moon altitude < 0° → `"none"`  
- phase fraction < 0.1 → `"none"`  
- otherwise bucket phase into crescent/half/gibbous/full

### 4.6 Stars  
`true` only when:  
- `sky_mode = "night"`  
- `moon = "none"`

---

## 5. Versioning  
The DSL includes a mandatory `version` field.

Rules:

1. New fields must be optional.  
2. Existing fields must not change semantics.  
3. Renderers must ignore unknown fields gracefully.  
4. Breaking changes require a major version increment.

---

## 6. Forward‑Compatible Extensions  
Future versions may add:

- `season_palette`  
- `star_density`  
- `cloud_type`  
- `tide_state`  
- `horizon_visibility`  

Extensions must follow the versioning rules above.

---

## 7. Interpreter Contract  
Any renderer must:

1. Accept a valid DSL JSON object.  
2. Treat all fields deterministically.  
3. Ignore unknown fields.  
4. Produce consistent output for identical DSL input.  
5. Fail gracefully on malformed input.

For deeper exploration:  
- scene DSL  
- rule engine  
- digital twin architecture

---

