# Dynamic Island Wallpaper  
A minimalist, data‑driven **digital twin of an island**, rendered as a dynamic desktop wallpaper.  
The system computes real‑world astronomical and environmental data locally, compresses it into a symbolic **scene DSL**, and renders a consistent island image using a deterministic **procedural compositor**.

---

## Overview  
Dynamic Island Wallpaper creates a living wallpaper that reflects:

- Real sun position (azimuth + altitude)  
- Real moon position and phase  
- Tide height  
- Wind strength  
- Wave intensity  
- Weather conditions  
- Time‑of‑day palette (day/sunset/night)  
- Daily rhythm animations (coffee, work start, callisthenics, evening, sleep)

Every 5 minutes, the system:

1. Computes sun & moon position locally  
2. Computes tide, wind, and weather state  
3. Passes raw telemetry to Prolog  
4. Prolog emits a symbolic **scene DSL JSON**  
5. The renderer applies deterministic overlays to a base island image  
6. The final image is set as the desktop wallpaper  

This produces a stable, ambient, low‑GPU digital twin of your day.

---

## Features  
- Local astronomical computation (no APIs)  
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
- Procedural rendering (no generative model)  
- Cross‑platform wallpaper setting  
- Extensible digital‑twin architecture  

---

## Project Structure  
```
dynamic_island_wallpaper/
│
├── docs/
│   ├── motivation.md          # Project motivation
│   ├── dsl-spec.md            # Formal scene DSL specification (v0.0.1)
│   ├── architecture.md        # System architecture & data flow
│   ├── telemetry.md           # Local astronomy + environment formulas
│   ├── rendering.md           # Procedural compositor & animation system
│   ├── roadmap.md             # Planned extensions
│   └── contributing.md        # Guidelines for contributors
│
├── src/
│   ├── telemetry/
│   │   ├── astronomy.py       # Sun/moon position + phase (local computation)
│   │   ├── weather.py         # Local weather logic
│   │   └── tide.py            # Tide height computation
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
│   └── main.py                # Main loop
│
├── assets/                    # Base island image + animation frames
├── tests/                     # Unit tests for DSL, rules, rendering
│
├── config.json                # User configuration
├── README.md                  # Project overview
├── CHANGELOG.md
└── LICENSE
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

### 1. Local Telemetry  
Every update cycle, the system computes:

- Solar altitude & azimuth  
- Moon altitude & phase  
- Tide height  
- Wind speed  
- Weather state  

No external APIs.  
All formulas are local and deterministic.

---

### 2. Prolog Scene Description (DSL)  
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

### 3. Procedural Rendering  
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

