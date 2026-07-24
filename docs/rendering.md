# Rendering  
Dynamic Island Wallpaper supports **two rendering modes**, each with different determinism guarantees:

1. **Deterministic Procedural Rendering**  
2. **Non‑Deterministic Generative Reference‑Image Rendering**

Determinism is binary:  
**a pipeline is deterministic or it is not.**  
This document makes that distinction explicit.

---

## 1. Rendering Overview  
The renderer consumes the symbolic **Scene DSL (v0.0.1)** and produces a wallpaper image.

The DSL contains *only symbolic meaning*:

- sky state  
- weather  
- tide  
- wind  
- waves  
- palette  
- daily rhythm  

The renderer interprets these symbols using one of two modes.

---

# 2. Procedural Rendering (Deterministic)

Procedural rendering is **strictly deterministic**.

> **Given the same DSL JSON + same base PNG → the output PNG is identical, byte‑for‑byte.**

There is no randomness, no sampling, no diffusion, no stochastic noise.

### 2.1 Base Image  
A fixed PNG containing:

- island silhouette  
- ocean baseline  
- palm tree neutral pose  
- sky gradient placeholders  

### 2.2 Deterministic Overlays  
Each DSL field maps to a fixed, deterministic transformation:

- **waterline mask** → `tide_state`  
- **wave texture** → `wave_intensity`  
- **tree lean transform** → `wind_strength`  
- **palette recolouring** → `island_palette`  
- **sun/moon/stars** → sky fields  
- **weather overlays** → `weather`  
- **character animations** → `daily_state`

### 2.3 Animation Frames  
Animations are deterministic frame sequences:

- morning coffee  
- work‑start sitting  
- break‑time callisthenics  
- evening wave  
- sleep‑time campfire extinguish  

No randomness is introduced.

### 2.4 Determinism Guarantee  
Procedural mode is **fully deterministic**.

---

# 3. Generative Reference‑Image Mode (Non‑Deterministic)

This mode uses a **reference image** and applies a **generative transformation** (e.g., diffusion‑based img2img).

This pipeline is **not deterministic**, even if:

- the seed is fixed  
- the model is fixed  
- the scheduler is fixed  
- the prompt is fixed  
- the reference image is fixed  
- the strength parameter is fixed  

### Why it is not deterministic  
Diffusion models introduce nondeterminism through:

- stochastic denoising  
- GPU kernel scheduling  
- floating‑point nondeterminism  
- latent sampling variance  
- hardware‑dependent execution paths  

Therefore:

> **Generative reference‑image mode cannot guarantee identical PNG output.**

This is a fundamental property of diffusion‑based systems.

### 3.1 When to use this mode  
Only when you want:

- stylistic variation  
- painterly reinterpretation  
- non‑procedural creativity  
- diffusion‑based enhancement of the base image

### 3.2 When NOT to use this mode  
When you require:

- reproducibility  
- testability  
- deterministic behaviour  
- byte‑for‑byte identical output

---

# 4. Renderer Selection  
The renderer is chosen in configuration:

```json
{
  "renderer_mode": "procedural"   // deterministic
}
```

or

```json
{
  "renderer_mode": "generative"   // non-deterministic
}
```

If omitted, **procedural** is the default.

---

# 5. Determinism Summary

| Rendering Mode | Deterministic? | Notes |
|----------------|----------------|-------|
| **Procedural compositor** | **Yes** | Same DSL + same base image → identical PNG |
| **Generative reference‑image** | **No** | Diffusion introduces unavoidable nondeterminism |

There is no “partially deterministic” mode.  
There is no “mostly deterministic” mode.  
Determinism is binary.

---

# 6. Integration With DSL  
Both rendering modes consume the same DSL JSON.

The DSL remains:

- symbolic  
- declarative  
- renderer‑agnostic  
- stable across versions  

Renderers must ignore unknown fields and treat the DSL as the authoritative semantic description.

---

# 7. Summary  
Dynamic Island Wallpaper supports two rendering pipelines:

- **Procedural (deterministic)** — stable, reproducible, testable  
- **Generative (non‑deterministic)** — creative, variable, diffusion‑based  

Your architecture now explicitly acknowledges the determinism boundary.

---

