# Project Roadmap

## 1. Purpose  
This roadmap outlines planned enhancements to the Dynamic Sky Wallpaper system.  
It focuses on expanding the **telemetry → DSL → render** pipeline while preserving determinism, modularity, and backward compatibility.

---

## 2. Guiding Principles

- **Determinism** — identical DSL input must always produce identical output.  
- **Symbolic First** — all new features must extend the DSL before touching rendering.  
- **Backward Compatibility** — DSL v1.0 must remain valid indefinitely.  
- **Modularity** — telemetry, interpretation, and rendering must remain isolated.  
- **Renderer Independence** — the DSL must support future renderers (shader, LoRA, procedural).

For deeper exploration:  
- digital twin architecture  
- scene DSL

---

## 3. Roadmap Overview

### Version 1.x — DSL & Rendering Enhancements  
Incremental improvements that do not break DSL v1.0.

### Version 2.x — DSL Extensions  
New symbolic fields added in a backward‑compatible way.

### Version 3.x — Multi‑Domain Digital Twin  
Generalising the pipeline beyond sky rendering.

---

## 4. Version 1.x — Near‑Term Enhancements

### 4.1 Seasonal Colour Palettes  
Add seasonal gradient logic based on date and latitude.  
DSL impact: none (handled in rendering).  
Rendering impact: palette selection rules.

### 4.2 Star Density Mapping  
Stars become denser when solar altitude is far below horizon.  
DSL impact: none.  
Rendering impact: starfield intensity.

### 4.3 Cloud Type Variation  
Use weather telemetry to distinguish:  
- cumulus  
- stratus  
- cirrus  
- storm clouds  
DSL impact: none (still `"weather"`).  
Rendering impact: cloud shape selection.

### 4.4 Horizon Visibility Rules  
Add dark horizon bands for approaching storms.  
DSL impact: none.  
Rendering impact: horizon shading.

### 4.5 Tide‑Driven Shoreline (Optional)  
If tide telemetry is enabled, adjust shoreline height.  
DSL impact: none (rendering only).  
Rendering impact: shoreline placement.

---

## 5. Version 2.x — DSL Extensions (Backward‑Compatible)

These features add new DSL fields but do not break existing ones.

### 5.1 `season_palette`  
Symbolic season category:  
`"summer" | "autumn" | "winter" | "spring"`  
Used for palette selection.

### 5.2 `star_density`  
Symbolic density bucket:  
`"none" | "low" | "medium" | "high"`  
Derived from solar altitude.

### 5.3 `cloud_type`  
Symbolic cloud classification:  
`"none" | "cumulus" | "stratus" | "cirrus" | "storm"`  
Derived from weather telemetry.

### 5.4 `horizon_visibility`  
Symbolic horizon clarity:  
`"clear" | "hazy" | "darkened"`  
Derived from weather + time.

### 5.5 `tide_state`  
Symbolic tide category:  
`"low" | "medium" | "high"`  
Derived from tide telemetry.

For deeper exploration:  
- extend the DSL

---

## 6. Version 3.x — Multi‑Domain Digital Twin

Generalise the pipeline to support other real‑world systems:

### 6.1 City Activity Twin  
Telemetry: traffic, weather, time.  
DSL: symbolic city state.  
Renderer: generative cityscape.

### 6.2 Personal Activity Twin  
Telemetry: CPU load, keyboard activity.  
DSL: symbolic focus/energy state.  
Renderer: ambient generative art.

### 6.3 Ocean/Tide Twin  
Telemetry: tide height, wind speed.  
DSL: symbolic ocean state.  
Renderer: generative shoreline.

### 6.4 Network Activity Twin  
Telemetry: bandwidth, latency.  
DSL: symbolic network state.  
Renderer: abstract flow visualisation.

For deeper exploration:  
- multi‑domain twin engine

---

## 7. Infrastructure & Tooling

### 7.1 Test Suite  
Add tests for:  
- DSL rule functions  
- prompt generation  
- renderer determinism  
- telemetry parsing

### 7.2 Config Validation  
Add schema validation for `config.json`.

### 7.3 Plugin System  
Allow custom telemetry modules and renderers.

### 7.4 Renderer Abstraction Layer  
Formalise a renderer interface so shaders or LoRAs can replace the tiny model.

---

## 8. Long‑Term Vision  
Dynamic Sky Wallpaper becomes a **general digital‑twin rendering framework**:

- Telemetry → DSL → Render  
- Deterministic  
- Modular  
- Extensible  
- Multi‑domain  

The sky twin is the first domain; others can follow.

---

## 9. Summary  
This roadmap outlines the evolution of the project from a minimalist sky twin to a general digital‑twin rendering framework.  
All changes must preserve determinism, modularity, and backward compatibility with DSL v1.0.

---

