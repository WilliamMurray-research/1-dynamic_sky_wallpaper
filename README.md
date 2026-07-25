# Dynamic Island Wallpaper  
## Project 1

**Start**: 22 July 2026 
**End**: - 

> Note: This project is intentionally scoped as a personal learning exercise in digital‑twin design, symbolic scene languages, Prolog rule systems, and deterministic rendering pipelines. It is architecturally opinionated but exploratory, serving as a sandbox for developing and refining system‑design skills.

A minimalist, data‑driven **digital twin of an island**, rendered as a dynamic desktop wallpaper.  
The system computes real‑world astronomical data locally, fetches environmental data from the **BOM API**, compresses everything into a symbolic **scene DSL**, and renders a consistent island image using a deterministic **procedural compositor**.  
An optional generative mode can apply a diffusion‑based transformation to a reference image, but this mode is **not deterministic**.

---

## Overview  
Dynamic Island Wallpaper creates a living wallpaper that reflects:

- Real sun position (azimuth + altitude)  
- Real moon position and phase  
- Tide height (BOM)  
- Wind strength (BOM)  
- Weather conditions (BOM)  
- Wave intensity  
- Time‑of‑day palette (day/sunset/night)  
- Daily rhythm animations (coffee, work start, callisthenics, evening, sleep)

Every 5 minutes, the system:

1. Computes sun & moon position locally  
2. Fetches tide, wind, and weather from the BOM API  
3. Passes raw telemetry to Prolog  
4. Prolog emits a symbolic **scene DSL JSON**  
5. The renderer applies deterministic overlays to a base island image  
6. The final image is set as the desktop wallpaper  

This produces a stable, ambient, low‑GPU digital twin of your day.

---

## Features  
- Local astronomical computation  
- BOM‑derived environmental telemetry  
- Deterministic symbolic scene DSL  
- Tide‑driven shoreline  
- Wind‑driven palm tree motion  
- Wave intensity based on wind + weather  
- Time‑of‑day palette (day/sunset/night)  
- Character animations for daily rhythm:  
  - Morning coffee  
  - Work start  
  - Break‑time callisthenics  
  - Evening wave  
  - Sleep‑time campfire extinguish  
- **Procedural rendering (deterministic)**  
- **Optional generative reference‑image mode (non‑deterministic)**  
- Cross‑platform wallpaper setting  
- Extensible digital‑twin architecture  

---

## Project Structure  
```
dynamic_island_wallpaper/
│
├── docs/
│   ├── motivation.md          # Why the project exists; design philosophy
│   ├── dsl-spec.md            # Formal scene DSL specification (v0.0.1)
│   ├── architecture.md        # Full system architecture & data flow
│   ├── telemetry.md           # Astronomy + BOM telemetry (deterministic)
│   ├── rendering.md           # Procedural compositor & generative mode
│   ├── roadmap.md             # Planned extensions & future versions
│   └── contributing.md        # Contributor guidelines & coding standards
│
├── src/
│   ├── telemetry/
│   │   ├── astronomy.py       # Sun/moon position + phase (local computation)
│   │   ├── bom_weather.py     # BOM weather + wind → numeric telemetry
│   │   └── bom_tide.py        # BOM tide height → numeric telemetry
│   │
│   ├── prolog/
│   │   ├── rules.pl           # Telemetry → symbolic scene rules
│   │   └── emit_json.pl       # Prolog → DSL JSON emitter
│   │
│   ├── renderer/
│   │   ├── compositor.py      # Base image + deterministic overlays
│   │   ├── palette.py         # Day/sunset/night recolouring
│   │   ├── waves.py           # Wave intensity overlays
│   │   ├── tree.py            # Palm tree wind transform
│   │   └── animations.py      # Daily rhythm animations
│   │
│   ├── wallpaper/
│   │   └── setter.py          # OS-specific wallpaper update
│   │
│   ├── config/
│   │   └── loader.py          # Config loader & validation
│   │
│   └── main.py                # Main loop: telemetry → Prolog → render → wallpaper
│
├── assets/                    # Base island image + overlays + animation frames
│
├── tests/                     # Unit tests for DSL, rules, telemetry, rendering
│   ├── test_rules.py
│   ├── test_emit_json.py
│   ├── test_astronomy.py
│   ├── test_bom_weather.py
│   ├── test_bom_tide.py
│   ├── test_palette.py
│   ├── test_waves.py
│   ├── test_tree.py
│   ├── test_animations.py
│   └── test_compositor.py
│
├── config.json                # User configuration (location, rhythm, BOM ID)
├── README.md                  # Project overview & quickstart
├── CHANGELOG.md               # Version history
└── LICENSE                    # Open-source license
```

---

## Scene DSL Specification (v0.0.1)  
The scene DSL is a symbolic description of the island environment.  
It is expressed in JSON, but JSON is only the carrier — the DSL is the **language**.

### Required Fields  
```json
{
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

  "daily_state": "<enum>",

  "version": "0.0.1"
}
```

### Field Definitions  
- **sunposition** — `"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`  
- **sun_height** — `"none" | "low" | "medium" | "high"`  
- **sky_mode** — `"night" | "dawn" | "day" | "dusk"`  
- **weather** — `"clear" | "cloudy" | "approaching_rain" | "rain"`  
- **moon** — `"none" | "crescent" | "half" | "gibbous" | "full"`  
- **stars** — `true | false`  

Island fields:  
- **tide_state** — `"low" | "medium" | "high"`  
- **wind_strength** — `"none" | "breeze" | "windy" | "strong"`  
- **wave_intensity** — `"calm" | "gentle" | "rough" | "storm"`  
- **island_palette** — `"day" | "sunset" | "night"`  

Daily rhythm:  
- **daily_state** —  
  `"morning_start" | "work_start" | "day_progress" | "break_time" | "evening" | "sleep_time"`

---

## How It Works

### 1. Telemetry  
Every update cycle, the system gathers:

- Solar altitude & azimuth (local computation)  
- Moon altitude & phase (local computation)  
- Tide height (BOM API)  
- Wind speed (BOM API)  
- Weather state (BOM API)

Astronomy is deterministic.  
BOM data is treated as deterministic input.

---

### 2. Prolog Scene Description (DSL)  
Prolog converts raw telemetry into symbolic categories and emits the DSL JSON.

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

This symbolic state is the **digital twin** of the island.

---

### 3. Procedural Rendering (Deterministic)  
The renderer applies deterministic overlays to a base island image:

- waterline mask (tide)  
- wave texture (wave intensity)  
- palm tree lean (wind)  
- palette recolouring  
- sun/moon/stars  
- weather overlays  
- character animations (daily_state)

No generative model.  
No randomness.  
Perfect style consistency.

---

### Optional Generative Mode (Non‑Deterministic)  
If enabled, a diffusion‑based img2img transformation is applied to a reference image, acting as a **style‑anchored, telemetry‑driven transformation layer** on top of the symbolic digital twin.  
This mode is **not deterministic**, even with fixed seeds.

---

### 4. Wallpaper Update  
The final PNG is saved and applied using OS‑specific commands.

---

## Installation

### Requirements  
- Python 3.10+  
- SWI‑Prolog  
- Pillow or similar image library  

### Setup  
```
git clone https://github.com/<yourname>/dynamic-island-wallpaper
cd dynamic-island-wallpaper
pip install -r requirements.txt
```

### Run  
```
python main.py
```

---

## Configuration  
`config.json`:

```json
{
  "location": {
    "lat": -33.185,
    "lon": 138.017
  },
  "updateintervalminutes": 5,
  "sleep_time": "23:00",
  "work_start": "09:00",
  "break_times": ["11:00", "15:00"],
  "wallpaper_output": "output/wallpaper.png"
}
```

---

## Rendering Rules

### Sun & Moon  
- Local astronomy formulas  
- Deterministic bucketing into symbolic fields  

### Island  
- Tide → waterline height  
- Wind → palm tree lean  
- Waves → ocean texture  
- Palette → recolouring  

### Daily Rhythm  
- Morning → coffee animation  
- Work start → sitting animation  
- Break → callisthenics  
- Evening → wave  
- Sleep → campfire extinguish  

---

## Roadmap  
- Seasonal palettes  
- Cloud type classification  
- Character emotion states  
- Multi‑domain digital‑twin support  
- Prolog explain‑why queries  
- Smooth animation interpolation  

---

## License  
MIT License

---

