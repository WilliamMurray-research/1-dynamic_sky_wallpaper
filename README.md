# Dynamic Sky Wallpaper  
A minimalist, data‑driven **digital twin of the sky**, rendered as a dynamic desktop wallpaper.  
The system polls real‑world astronomical and weather data, compresses it into a symbolic **scene DSL**, and renders a consistent sky image using a tiny local generative model.

---

## Overview  
Dynamic Sky Wallpaper creates a living wallpaper that reflects:

- Real sun position (azimuth + altitude)  
- Seasonal sun height  
- Dawn/dusk colour transitions  
- Weather conditions  
- Moon visibility and phase  
- Star visibility when the moon is absent  

Every 5 minutes, the system:

1. Fetches real‑world data  
2. Converts it into a symbolic **scene description**  
3. Generates a deterministic prompt  
4. Renders a minimalist sky image using a tiny model  
5. Sets the image as the desktop wallpaper  

This keeps GPU usage extremely low while producing a continuously updated sky.

---

## Features  
- Real astronomical positioning  
- Seasonal solar altitude  
- Rule‑based sky colour gradients  
- Weather‑driven cloud and rain rendering  
- Moon phase logic  
- Starfield when moon is absent  
- Tiny model inference (<1s)  
- Cross‑platform wallpaper setting  
- Formalised **scene DSL** for deterministic rendering  
- Extensible digital‑twin architecture  

---

## Project Structure  
```
dynamic-sky-wallpaper/
│
├── api/
│   ├── sun_moon.py        # Solar & lunar data fetch
│   ├── weather.py         # Weather API fetch
│   └── tides.py           # Optional tide data
│
├── scene/
│   ├── builder.py         # Telemetry → DSL scene JSON
│   └── rules.py           # Semantic rules (sun pos, sky mode, etc.)
│
├── model/
│   ├── prompt.py          # DSL → deterministic prompt
│   └── render.py          # Tiny model renderer
│
├── wallpaper/
│   └── setter.py          # OS-specific wallpaper update
│
├── main.py                # Main loop
└── README.md
```

---

## Scene DSL Specification (v1.0)  
The scene DSL is a symbolic description of the sky.  
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
  "version": "1.0"
}
```

### Field Definitions  
- **sunposition** — `"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`  
- **sun_height** — `"none" | "low" | "medium" | "high"`  
- **sky_mode** — `"night" | "dawn" | "day" | "dusk"`  
- **weather** — `"clear" | "cloudy" | "approaching_rain" | "rain"`  
- **moon** — `"none" | "crescent" | "half" | "gibbous" | "full"`  
- **stars** — `true | false`  

### Semantic Rules  
- Sun below horizon → `sunposition = "none"`  
- Solar altitude buckets → `low`, `medium`, `high`  
- Dawn/dusk determined by altitude ± azimuth  
- Moon below horizon → `moon = "none"`  
- Stars visible only when `moon = "none"` and `sky_mode = "night"`  

For deeper exploration:  
- scene DSL  
- rule engine  
- digital twin architecture

---

## How It Works

### 1. API Polling  
Every update cycle, the system fetches:

- Solar altitude & azimuth  
- Moon altitude & phase  
- Weather conditions  
- Optional tide height  

APIs may include astronomical services, weather providers, or local computation libraries.

---

### 2. Scene Description (DSL)  
Example:

```json
{
  "sunposition": "bottomright",
  "sun_height": "low",
  "sky_mode": "dawn",
  "weather": "approaching_rain",
  "moon": "none",
  "stars": true,
  "version": "1.0"
}
```

This symbolic state is the **digital twin** of the sky.

---

### 3. Prompt Generation  
The DSL is converted into a deterministic prompt:

```
Minimalist sky wallpaper.
Soft dawn gradient.
Sun low in the bottom right.
Distant rain clouds.
No moon. Stars visible.
```

No randomness. No creativity.  
The model acts as a **renderer**, not an artist.

---

### 4. Tiny Model Rendering  
A small local model (SD‑Tiny, SD‑Mini, etc.) renders:

- Gradient sky  
- Sun circle  
- Moon phase  
- Cloud shapes  
- Rain streaks  
- Stars  

Inference time: ~0.5–1.5 seconds.

---

### 5. Wallpaper Update  
The generated image is saved and applied using OS‑specific commands.

---

## Installation

### Requirements  
- Python 3.10+  
- A tiny local image model  
- API keys (if required)

### Setup  
```
git clone https://github.com/<yourname>/dynamic-sky-wallpaper
cd dynamic-sky-wallpaper
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
  "model_path": "models/sd-tiny",
  "wallpaper_output": "output/wallpaper.png"
}
```

---

## Rendering Rules

### Sun  
- Sunrise → bottom right  
- Sunset → bottom left  
- Summer → high arc  
- Winter → low arc  

### Sky  
- Dawn/dusk → warm gradient  
- Day → blue gradient  
- Night → dark blue/black  

### Weather  
- Clear → no clouds  
- Rain → rain streaks  
- Approaching rain → dark horizon clouds  

### Moon  
- Below horizon → none  
- New moon → none  
- Otherwise → correct phase  

### Stars  
- Visible only when moon is absent  

---

## Roadmap  
- Seasonal palettes  
- Star density based on solar elevation  
- Tide‑driven shoreline height  
- Custom LoRA for consistent style  
- GPU/CPU fallback modes  
- Multi‑domain digital‑twin support  
- Generalised telemetry→DSL pipeline  

Explore generalisation:  
- digital twin framework  
- multi‑domain twin engine

---

## License  
MIT License

---

