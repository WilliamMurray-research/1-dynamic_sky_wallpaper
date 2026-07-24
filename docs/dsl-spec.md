# Scene DSL Specification — **v0.0.1**

## 1. Purpose  
The **v0.0.1 Scene DSL** defines a complete symbolic description of the island‑based digital twin.  
It is renderer‑agnostic, deterministic, and produced entirely by Prolog.  
Python simply consumes the JSON and renders the scene.

For deeper exploration:  
- scene DSL  
- rule engine

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

All fields are symbolic.  
No numeric telemetry appears in the DSL.

---

## 3. Sky & Weather Fields

### **sunposition**  
Symbolic solar azimuth bucket.  
Domain:  
`"none" | "bottomleft" | "bottomright" | "midleft" | "midright" | "topleft" | "topright"`

### **sun_height**  
Symbolic solar altitude bucket.  
Domain:  
`"none" | "low" | "medium" | "high"`

### **sky_mode**  
Time‑of‑day category.  
Domain:  
`"night" | "dawn" | "day" | "dusk"`

### **weather**  
Symbolic weather state.  
Domain:  
`"clear" | "cloudy" | "approaching_rain" | "rain"`

### **moon**  
Visible lunar phase.  
Domain:  
`"none" | "crescent" | "half" | "gibbous" | "full"`

### **stars**  
Star visibility.  
Domain:  
`true | false`

Explore these via sky rules.

---

## 4. Island Environmental Fields

### **tide_state**  
Symbolic tide height.  
Domain:  
`"low" | "medium" | "high"`

### **wind_strength**  
Symbolic wind intensity.  
Domain:  
`"none" | "breeze" | "windy" | "strong"`

### **wave_intensity**  
Symbolic ocean surface state.  
Domain:  
`"calm" | "gentle" | "rough" | "storm"`

### **island_palette**  
Colour theme for the island scene.  
Domain:  
`"day" | "sunset" | "night"`

Explore these via island rules.

---

## 5. Daily Rhythm Fields (Character Animations)

### **daily_state**  
Symbolic daily‑rhythm cue controlling character animation overlays.

Domain:  
- `"morning_start"` — person with coffee  
- `"work_start"` — person sitting down  
- `"day_progress"` — normal island scene  
- `"break_time"` — callisthenics animation  
- `"evening"` — person waving good night  
- `"sleep_time"` — campfire being put out  

Explore this via daily rhythm.

---

## 6. Semantic Rules (Telemetry → DSL)

These rules are implemented in Prolog and guarantee deterministic symbolic output.

### Sun height  
- alt < 0° → `"none"`  
- alt < 10° → `"low"`  
- alt < 35° → `"medium"`  
- alt ≥ 35° → `"high"`

### Sky mode  
- alt < −6° → `"night"`  
- −6° ≤ alt ≤ 6° → `"dawn"` or `"dusk"`  
- alt > 6° → `"day"`

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

## 7. Versioning Rules

- All fields are required in v0.0.1.  
- Future versions must remain backward‑compatible.  
- Renderers must ignore unknown fields gracefully.  
- Prolog is the authoritative source of truth.

---

## 8. Summary  
DSL v0.0.1 is a complete symbolic description of your island‑based digital twin:

- sky  
- weather  
- tide  
- wind  
- waves  
- palette  
- daily‑rhythm character animations  

It is deterministic, renderer‑agnostic, and perfectly suited for Prolog emission and procedural animation overlays.

---

