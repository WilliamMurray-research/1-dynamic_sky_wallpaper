# Architecture  
Dynamic Island Wallpaper is a deterministic **telemetry → semantics → rendering** pipeline.  
It produces a symbolic JSON scene using **Prolog**, then renders a stable island wallpaper using a **procedural compositor**.

The system is intentionally modular:

```
Telemetry → Prolog Semantic Engine → Scene DSL (JSON) → Renderer → Wallpaper
```

Each layer is isolated, testable, and replaceable.

---

## 1. System Overview  
The architecture is built around four principles:

- **Determinism** — identical inputs produce identical outputs  
- **Symbolic Semantics** — all meaning is encoded in the DSL  
- **Renderer Independence** — any renderer can consume the DSL  
- **Ambient Cues** — the wallpaper conveys time and environment passively  

The system is not a generative art pipeline.  
It is a **digital twin** of a small island environment.

Explore:  
- scene DSL  
- rule engine

---

## 2. Telemetry Layer  
Telemetry is computed **locally**, without external APIs.

### 2.1 Astronomy  
The system computes:

- solar altitude  
- solar azimuth  
- lunar altitude  
- lunar phase  
- sunrise/sunset times  

These values are derived from standard astronomical formulas.

### 2.2 Environment  
The system computes:

- tide height  
- wind speed  
- weather state  

These are simple deterministic formulas or local heuristics.

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

Explore:  
- astronomy computation

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

Explore:  
- Prolog JSON emitter

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

Full spec:  
- DSL v0.0.1

---

## 5. Procedural Renderer  
The renderer consumes the DSL JSON and produces a deterministic PNG.

### 5.1 Base Image  
A single base PNG contains:

- island silhouette  
- ocean baseline  
- palm tree neutral pose  
- sky gradient placeholders  

### 5.2 Deterministic Overlays  
The renderer applies overlays based on DSL fields:

- **waterline mask** → `tide_state`  
- **wave texture** → `wave_intensity`  
- **tree lean transform** → `wind_strength`  
- **palette recolouring** → `island_palette`  
- **sun/moon/stars** → sky fields  
- **weather overlays** → `weather`  
- **character animations** → `daily_state`

### 5.3 Animation System  
Animations are frame sequences or sprite sheets:

- morning coffee  
- sitting down to work  
- callisthenics  
- evening wave  
- campfire extinguish  

The renderer composites these frames on top of the base scene.

Explore:  
- procedural renderer  
- animation system

---

## 6. Wallpaper Module  
The final PNG is written to disk and applied using OS‑specific commands.

This module is intentionally simple and replaceable.

---

## 7. Data Flow Diagram

```
+------------------+
|   Telemetry      |
| (astronomy/env)  |
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
| (procedural)     |
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
Dynamic Island Wallpaper is a deterministic digital twin built from:

- local telemetry  
- Prolog semantics  
- symbolic DSL  
- procedural rendering  
- ambient daily‑rhythm cues  

It is designed for stability, clarity, and long‑term extensibility.

---


- **dsl-spec.md**  

Just tell me which file you want next.
