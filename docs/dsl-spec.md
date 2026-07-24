# Scene DSL Specification  
**Version: 0.0.1**

Dynamic Island Wallpaper uses a symbolic **Scene DSL** to describe the state of a small island environment.  
The DSL is **declarative**, **finite**, and **renderer‑agnostic**.  
It contains **no numeric telemetry**, **no rendering instructions**, and **no procedural or generative directives**.

The DSL is the *semantic contract* between the Prolog engine and any renderer.

Renderers may be:

- **deterministic** (procedural compositor), or  
- **non‑deterministic** (generative reference‑image transformation)

The DSL itself remains deterministic regardless of renderer choice.

---

## 1. Purpose  
The Scene DSL provides a stable, symbolic description of:

- sky state  
- weather  
- tide  
- wind  
- waves  
- palette  
- daily rhythm cues  

It is designed to be:

- **minimal**  
- **predictable**  
- **easy to version**  
- **easy to interpret**  
- **independent of rendering technology**

---

## 2. DSL Structure  
A valid scene description is a JSON object:

```json
{
  "version": "0.0.1",

  "sunposition": "<enum>",
  "sun_height": "<enum>",
  "sky_mode": "<enum>",
  "weather": "<enum>",
  "moon": "<enum>",
  "stars": "<boolean>",

  "tide_state": "<enum>",
  "wind_strength": "<enum>",
  "wave_intensity": "<enum>",
  "island_palette": "<enum>",

  "daily_state": "<enum>"
}
```

All fields are **required** in v0.0.1.

---

## 3. Sky & Weather Fields

### `sunposition`
Symbolic solar azimuth bucket.

Values:  
`"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`

### `sun_height`
Symbolic solar altitude bucket.

Values:  
`"none" | "low" | "medium" | "high"`

### `sky_mode`
Time‑of‑day category.

Values:  
`"night" | "dawn" | "day" | "dusk"`

### `weather`
Symbolic weather state.

Values:  
`"clear" | "cloudy" | "approaching_rain" | "rain"`

### `moon`
Visible lunar phase.

Values:  
`"none" | "crescent" | "half" | "gibbous" | "full"`

### `stars`
Star visibility.

Values:  
`true | false`

---

## 4. Island Environmental Fields

### `tide_state`
Symbolic tide height.

Values:  
`"low" | "medium" | "high"`

### `wind_strength`
Symbolic wind intensity.

Values:  
`"none" | "breeze" | "windy" | "strong"`

### `wave_intensity`
Symbolic ocean surface state.

Values:  
`"calm" | "gentle" | "rough" | "storm"`

### `island_palette`
Colour theme for the island scene.

Values:  
`"day" | "sunset" | "night"`

---

## 5. Daily Rhythm Field

### `daily_state`
Symbolic daily‑rhythm cue controlling character animations.

Values:  
- `"morning_start"` — coffee animation  
- `"work_start"` — sitting animation  
- `"day_progress"` — neutral scene  
- `"break_time"` — callisthenics animation  
- `"evening"` — wave animation  
- `"sleep_time"` — campfire extinguish animation  

This field does **not** specify animation frames or rendering behaviour.  
It is purely symbolic.

---

## 6. Semantic Rules (Telemetry → DSL)

These rules are implemented in Prolog.  
They convert raw numeric telemetry into symbolic categories.

### Solar altitude → `sun_height`
- alt < 0° → `"none"`  
- alt < 10° → `"low"`  
- alt < 35° → `"medium"`  
- alt ≥ 35° → `"high"`

### Solar azimuth + altitude → `sunposition`
Buckets are hemisphere‑aware and renderer‑agnostic.

### Sky mode
- alt < −6° → `"night"`  
- −6° ≤ alt ≤ 6° → `"dawn"` or `"dusk"`  
- alt > 6° → `"day"`

### Moon visibility
- moon_alt < 0° → `"none"`  
- otherwise → bucket phase

### Stars
- visible only when `moon = "none"` and `sky_mode = "night"`

### Tide
- < 0.5 m → `"low"`  
- 0.5–1.2 m → `"medium"`  
- > 1.2 m → `"high"`

### Wind
- < 2 m/s → `"none"`  
- 2–5 m/s → `"breeze"`  
- 5–10 m/s → `"windy"`  
- > 10 m/s → `"strong"`

### Waves
Derived from wind + weather.

### Palette
Derived from sky_mode.

### Daily rhythm
Derived from user schedule + sunrise/sunset.

---

## 7. Renderer Independence  
The DSL does **not** assume a deterministic renderer.

Two renderer modes exist:

### **Procedural compositor (deterministic)**  
- Same DSL → same PNG  
- Byte‑for‑byte reproducible  
- No randomness  
- No diffusion  
- No sampling

### **Generative reference‑image mode (non‑deterministic)**  
- Uses diffusion or img2img  
- Output varies even with fixed seeds  
- GPU nondeterminism applies  
- Not reproducible byte‑for‑byte

The DSL remains valid for both modes.

---

## 8. Versioning  
- DSL versions are immutable  
- Renderers must ignore unknown fields  
- Prolog rules may evolve without breaking old DSLs  
- Telemetry sources may change without affecting DSL structure  

---

## 9. Summary  
The Scene DSL v0.0.1 is:

- symbolic  
- deterministic  
- declarative  
- renderer‑agnostic  
- stable  
- minimal  
- extensible  

It is the semantic backbone of Dynamic Island Wallpaper.

---

