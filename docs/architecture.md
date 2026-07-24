# Architecture  
Dynamic Island Wallpaper is a **telemetry → semantics → rendering** pipeline.  
It produces a symbolic JSON scene using **Prolog**, then renders an island wallpaper using either:

- a **deterministic procedural compositor**, or  
- a **non‑deterministic generative transformation** applied to a reference image.

Because determinism is binary, the architecture explicitly distinguishes these two modes.

The system is intentionally modular:

```
Telemetry → Prolog Semantic Engine → Scene DSL (JSON) → Renderer → Wallpaper
```

Each layer is isolated, testable, and replaceable.

---

## 1. System Overview  
The architecture is built around four principles:

- **Determinism (procedural mode)** — identical inputs produce identical outputs  
- **Symbolic Semantics** — all meaning is encoded in the DSL  
- **Renderer Independence** — any renderer can consume the DSL  
- **Ambient Cues** — the wallpaper conveys time and environment passively  

When using the **procedural compositor**, the system is fully deterministic.  
When using a **generative transformation** (e.g., img2img) with a reference image, the output is **not deterministic**, even if seeded, due to inherent stochasticity in diffusion‑based pipelines.

The system is a **digital twin** of a small island environment.

---

## 2. Telemetry Layer  
Telemetry is a combination of **local computation** and **external API data**.

### 2.1 Astronomy  
The system computes:

- solar altitude  
- solar azimuth  
- lunar altitude  
- lunar phase  
- sunrise/sunset times  

These values are derived from standard astronomical formulas.

### 2.2 Environment (BOM API)  
The system fetches:

- tide height  
- wind speed  
- weather state  

These values are retrieved from the Bureau of Meteorology (BOM) API and normalised into internal numeric codes or units.

### 2.3 Output  
Telemetry produces **raw numeric facts**, never symbolic categories.

Example (Python → Prolog facts):

```
sun_alt(12.4).
sun_az(145.0).
moon_alt(-5.0).
moon_phase(0.62).
tide_height(0.8).
wind_speed(4.2).
weather_code(2).
```

---

## 3. Prolog Semantic Engine  
Prolog is the **authoritative semantic layer**.

It receives raw telemetry and produces:

- symbolic categories  
- constraint‑checked scene state  
- complete DSL JSON

### 3.1 Symbolic Bucketing  
Prolog converts numeric telemetry into symbolic DSL fields:

- `sun_height`  
- `sunposition`  
- `sky_mode`  
- `moon`  
- `stars`  
- `tide_state`  
- `wind_strength`  
- `wave_intensity`  
- `island_palette`  
- `daily_state`

### 3.2 Constraint Checking  
Prolog enforces rules such as:

- if `sky_mode = night` → `sun_height = none`  
- if `moon = none` → `stars = true` allowed  
- if `wind_strength = strong` → `wave_intensity ≠ calm`  
- if `Time >= SleepTime` → `daily_state = sleep_time`

### 3.3 JSON Emission  
Prolog emits the final DSL JSON as a single atom.

Example:

```json
{
  "sunposition": "topright",
  "sun_height": "high",
  "sky_mode": "day",
  "weather": "clear",
  "moon": "none",
  "stars": false,

  "tide_state": "medium",
  "wind_strength": "breeze",
  "wave_intensity": "gentle",
  "island_palette": "day",

  "daily_state": "break_time",

  "version": "0.0.1"
}
```

---

## 4. Scene DSL (v0.0.1)  
The DSL is a **symbolic snapshot** of the island environment.

It contains no numeric telemetry and no rendering instructions.  
It is purely declarative.

Fields include:

- sky state  
- weather  
- tide  
- wind  
- waves  
- palette  
- daily rhythm  

---

## 5. Renderer  
The renderer consumes the DSL JSON and produces the wallpaper image.  
There are **two rendering modes**, each with different determinism properties.

---

### 5.1 Deterministic Procedural Mode  
This mode is **strictly deterministic**.

A single base PNG contains:

- island silhouette  
- ocean baseline  
- palm tree neutral pose  
- sky gradient placeholders  

The renderer applies deterministic overlays based on DSL fields:

- **waterline mask** → `tide_state`  
- **wave texture** → `wave_intensity`  
- **tree lean transform** → `wind_strength`  
- **palette recolouring** → `island_palette`  
- **sun/moon/stars** → sky fields  
- **weather overlays** → `weather`  
- **character animations** → `daily_state`

Animations are fixed frame sequences or sprite sheets.

Given the same DSL + same base image → **the output PNG is identical**.

---

### 5.2 Generative Reference‑Image Mode (Non‑Deterministic)  
If the renderer uses a **reference image** and applies a **generative transformation** (e.g., diffusion‑based img2img), the output is **not deterministic**, even if:

- the seed is fixed  
- the model is fixed  
- the scheduler is fixed  
- the prompt is fixed  
- the reference image is fixed  

GPU execution, floating‑point nondeterminism, and stochastic denoising introduce unavoidable variation.

This mode is optional and explicitly non‑deterministic.

---

## 6. Wallpaper Module  
The final PNG is written to disk and applied using OS‑specific commands.

This module is intentionally simple and replaceable.

---

## 7. Data Flow Diagram

```
+------------------+
|   Telemetry      |
| (astronomy/BOM)  |
+--------+---------+
         |
         v
+------------------+
|   Prolog Engine  |
|  (semantics)     |
+--------+---------+
         |
         v
+------------------+
|   Scene DSL      |
|    (JSON)        |
+--------+---------+
         |
         v
+------------------+
|   Renderer       |
| procedural OR    |
| generative       |
+--------+---------+
         |
         v
+------------------+
|   Wallpaper      |
+------------------+
```

---

## 8. Versioning  
The architecture follows strict versioning rules:

- DSL versions are immutable  
- renderers must ignore unknown fields  
- Prolog rules evolve without breaking old DSLs  
- telemetry formulas remain stable  

---

## 9. Summary  
Dynamic Island Wallpaper is a digital twin built from:

- local astronomy  
- BOM environmental telemetry  
- Prolog semantics  
- symbolic DSL  
- procedural or generative rendering  
- ambient daily‑rhythm cues  

**Procedural mode is deterministic.**  
**Generative mode is not.**

---

