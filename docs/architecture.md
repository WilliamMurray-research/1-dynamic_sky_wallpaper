# Architecture Overview

## 1. Purpose  
This document describes the architecture of the Dynamic Sky Wallpaper system.  
The system is built as a **minimal digital twin**: real‑world telemetry is transformed into a symbolic **scene DSL**, interpreted deterministically, and rendered into a sky image using a tiny local model.

The architecture is intentionally modular, extensible, and easy to reason about.

---

## 2. High‑Level Pipeline  
The system follows a five‑stage pipeline:

1. **Telemetry** — Fetch real‑world data  
2. **Interpretation** — Convert raw data into semantic categories  
3. **Scene DSL** — Produce a symbolic JSON description  
4. **Prompt Generation** — Convert DSL → deterministic text prompt  
5. **Rendering** — Generate the sky image using a tiny model  
6. **Wallpaper Update** — Apply the rendered image to the OS

This pipeline is deterministic: identical telemetry produces identical output.

For deeper exploration:  
- digital twin architecture  
- scene DSL

---

## 3. Module Layout  
All implementation lives under `src/`:

```
src/
│
├── api/            # Telemetry layer
├── scene/          # Interpretation + DSL construction
├── model/          # Prompt + rendering
├── wallpaper/      # OS integration
└── main.py         # Pipeline orchestration
```

Each module has a single responsibility.

---

## 4. Telemetry Layer (`src/api/`)  
The telemetry layer fetches real‑world data:

- Solar altitude and azimuth  
- Moon altitude and phase  
- Weather conditions  
- Optional tide height  

Modules:

- `sun_moon.py`  
- `weather.py`  
- `tides.py`  

Telemetry must return **raw numeric or categorical data**, not symbolic DSL values.

For details:  
- telemetry

---

## 5. Interpretation Layer (`src/scene/`)  
This layer converts raw telemetry into **semantic categories** using deterministic rules.

Modules:

- `rules.py` — semantic mapping functions  
- `builder.py` — constructs the final DSL JSON

Example:

```python
scene = {
    "sunposition": rules.sun_position(azimuth, altitude),
    "sun_height": rules.sun_height(altitude),
    "sky_mode": rules.sky_mode(altitude, azimuth),
    "weather": rules.weather_mode(weather_data),
    "moon": rules.moon_mode(moon_alt, moon_phase),
    "stars": rules.star_visibility(moon_alt, moon_phase, altitude),
    "version": "1.0"
}
```

This layer is the **interpreter** for the DSL.

---

## 6. Scene DSL (`docs/dsl-spec.md`)  
The DSL is a symbolic description of the sky.  
It is stable, versioned, and designed for forward‑compatible extension.

The DSL is the **contract** between the interpretation layer and the rendering layer.

For full specification:  
- DSL spec

---

## 7. Prompt Generation (`src/model/prompt.py`)  
The DSL is converted into a deterministic text prompt.

Rules:

- No randomness  
- No creative phrasing  
- No synonyms  
- One‑to‑one mapping from DSL → prompt lines

Example:

```
Minimalist sky wallpaper.
Day gradient.
Sun high in the top right.
Clear weather.
Moon: none.
Stars: false.
```

This ensures consistent rendering across updates.

---

## 8. Rendering Layer (`src/model/render.py`)  
A tiny local model (e.g., SD‑Tiny) renders the sky image.

Requirements:

- Fixed resolution  
- Fixed sampler  
- Fixed number of steps  
- Deterministic seed  
- No stylistic variation unless configured

The model acts as a **renderer**, not a creative generator.

For deeper exploration:  
- generative renderer design

---

## 9. Wallpaper Layer (`src/wallpaper/`)  
This layer applies the rendered image to the OS.

- macOS: `osascript`  
- Linux: `gsettings`, `feh`, or DE‑specific commands  
- Windows: registry + `ctypes`

This module must be isolated so users can extend or replace it.

---

## 10. Main Orchestrator (`src/main.py`)  
The main loop coordinates the pipeline:

1. Load config  
2. Fetch telemetry  
3. Build DSL  
4. Generate prompt  
5. Render image  
6. Set wallpaper  
7. Sleep until next update

This file contains no business logic — only orchestration.

---

## 11. Extensibility  
The architecture supports:

- New telemetry sources  
- New DSL fields  
- New rendering rules  
- New palettes  
- New output formats  
- Multi‑domain digital twins  

Extensions must follow DSL versioning rules.

For generalisation:  
- multi‑domain twin engine

---

## 12. Design Principles  
The architecture follows four principles:

### 1. **Determinism**  
Same input → same output.

### 2. **Separation of Concerns**  
Telemetry, interpretation, rendering, and OS integration are isolated.

### 3. **Symbolic Compression**  
Raw data is reduced to a small, stable DSL.

### 4. **Renderer Independence**  
Any renderer (tiny model, shader, procedural engine) can interpret the DSL.

---

## 13. Summary  
Dynamic Sky Wallpaper is a modular digital‑twin system built around a symbolic DSL.  
Its architecture is designed for clarity, determinism, and extensibility, enabling future growth into multi‑domain telemetry→DSL→render pipelines.

---

