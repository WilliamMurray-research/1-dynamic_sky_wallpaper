# Scene DSL Extension (v1.1)

## 1. Purpose  
DSL v1.1 expands the sky‑only digital twin into an **island‑based environmental twin**.  
It introduces symbolic fields for:

- tide height  
- wind strength  
- wave intensity  
- palette mode (day/sunset/night)

These fields support your v1 cartoon‑island renderer.

---

## 2. New Fields (v1.1)

### 2.1 **`tide_state`**  
Symbolic tide height.

**Domain:**  
`"low" | "medium" | "high"`

**Semantics:**  
Derived from raw tide telemetry (`tide_height`).

**Interpreter Contract:**  
Controls waterline position relative to the island.

---

### 2.2 **`wind_strength`**  
Symbolic wind intensity.

**Domain:**  
`"none" | "breeze" | "windy" | "strong"`

**Semantics:**  
Derived from wind speed telemetry.

**Interpreter Contract:**  
Controls palm tree lean angle and motion cues.

---

### 2.3 **`wave_intensity`**  
Symbolic ocean surface state.

**Domain:**  
`"calm" | "gentle" | "rough" | "storm"`

**Semantics:**  
Derived from wind_strength + weather.

**Interpreter Contract:**  
Controls wave height and ocean texture.

---

### 2.4 **`island_palette`**  
Symbolic colour theme for the island scene.

**Domain:**  
`"day" | "sunset" | "night"`

**Semantics:**  
Derived from `sky_mode`.

**Interpreter Contract:**  
Controls global colour palette (sky, water, island).

---

## 3. Updated DSL Structure (v1.1)

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

All v1.0 fields remain unchanged.

---

## 4. Semantic Rules (Telemetry → DSL)

### 4.1 Tide → `tide_state`
- tide_height < 0.5 m → `"low"`  
- 0.5–1.2 m → `"medium"`  
- > 1.2 m → `"high"`

### 4.2 Wind → `wind_strength`
- speed < 2 m/s → `"none"`  
- 2–5 m/s → `"breeze"`  
- 5–10 m/s → `"windy"`  
- > 10 m/s → `"strong"`

### 4.3 Waves → `wave_intensity`
Derived from wind + weather:

- wind none/breeze + clear → `"calm"`  
- breeze/windy + cloudy → `"gentle"`  
- windy + approaching_rain → `"rough"`  
- strong + rain → `"storm"`

### 4.4 Palette → `island_palette`
- sky_mode = day → `"day"`  
- sky_mode = dawn/dusk → `"sunset"`  
- sky_mode = night → `"night"`

---

## 5. Backward Compatibility  
DSL v1.1 follows strict compatibility rules:

- All new fields are optional.  
- v1.0 renderers ignore unknown fields.  
- v1.0 scenes remain valid.  
- No semantics of existing fields changed.

This ensures stable evolution.

---

## 6. Renderer Contract Additions  
Renderers must:

- adjust waterline based on `tide_state`  
- lean palm tree based on `wind_strength`  
- adjust wave height based on `wave_intensity`  
- select palette based on `island_palette`  

All behaviour must remain deterministic.

---

## 7. Summary  
DSL v1.1 introduces symbolic environmental cues for your cartoon‑island renderer:

- tide  
- wind  
- waves  
- palette  

These additions preserve the DSL’s clarity, determinism, and extensibility while enabling a richer, more meaningful ambient scene.

---

