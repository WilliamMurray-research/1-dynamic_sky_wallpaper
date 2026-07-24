# Rendering Pipeline Specification

## 1. Purpose  
The rendering pipeline converts a symbolic **scene DSL** into a deterministic sky image.  
The renderer is intentionally minimal: it does not “create art,” it **renders** a scene description.  
This document defines the prompt rules, model configuration, deterministic behaviour, and output requirements.

---

## 2. Rendering Overview  
Rendering consists of three stages:

1. **Prompt Generation** — DSL → deterministic text prompt  
2. **Model Invocation** — tiny model renders the scene  
3. **Output Handling** — save image and pass to wallpaper module

The renderer must produce identical output for identical DSL input.

For deeper exploration:  
- generative renderer design  
- scene DSL

---

## 3. Prompt Generation (`src/model/prompt.py`)

### 3.1 Purpose  
Convert DSL fields into a fixed, predictable text prompt.  
No randomness, synonyms, or stylistic variation.

### 3.2 Prompt Structure  
The prompt is composed of short declarative lines:

```
Minimalist sky wallpaper.
<sky_mode> gradient.
Sun: <sun_height> at <sunposition>.
Weather: <weather>.
Moon: <moon>.
Stars: <true|false>.
```

### 3.3 Rules  
- Each DSL field maps to exactly one line.  
- No adjectives beyond the defined vocabulary.  
- No creative phrasing.  
- No conditional grammar.  
- No model-specific keywords (e.g., “masterpiece”, “ultra-detailed”).  
- The prompt must remain stable across versions unless the DSL changes.

### 3.4 Example  
DSL:

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

Prompt:

```
Minimalist sky wallpaper.
Dawn gradient.
Sun: low at bottomright.
Weather: approaching_rain.
Moon: none.
Stars: true.
```

---

## 4. Model Rendering (`src/model/render.py`)

### 4.1 Model Requirements  
The renderer uses a **tiny local model** (e.g., SD‑Tiny, SD‑Mini).  
Requirements:

- Deterministic seed  
- Fixed sampler  
- Fixed number of steps  
- Fixed resolution  
- No randomness  
- No external dependencies beyond the model

### 4.2 Deterministic Configuration  
Recommended defaults:

- Resolution: `1920x1080`  
- Steps: `20–30`  
- Sampler: `Euler` or `DDIM`  
- Seed: fixed integer (e.g., `42`)  
- CFG scale: low (e.g., `3–5`) to maintain minimalism

These values must not change across updates unless explicitly versioned.

### 4.3 Renderer Responsibilities  
The renderer must:

1. Accept the deterministic prompt  
2. Produce a single image  
3. Apply no post‑processing beyond resizing  
4. Return the image path to the wallpaper module

### 4.4 Renderer Independence  
The DSL is renderer‑agnostic.  
Any future renderer (shader, procedural engine, LoRA‑based model) must follow the same interpreter contract:

- deterministic  
- symbolic input  
- stable output  
- no creative deviation

---

## 5. Output Handling

### 5.1 File Format  
The renderer must output:

- PNG format  
- sRGB colour  
- No metadata beyond resolution

### 5.2 File Location  
Output path is defined in `config.json`:

```json
"wallpaper_output": "output/wallpaper.png"
```

### 5.3 Handoff  
The wallpaper module receives the final image path and applies it to the OS.

---

## 6. Error Handling  
Rendering errors must:

- never crash the main loop  
- return a structured error object  
- allow the system to retry on next cycle  
- never produce partial or corrupted images

If rendering fails, the wallpaper should not be updated.

---

## 7. Determinism Requirements  
The renderer must guarantee:

1. Same DSL → same prompt  
2. Same prompt → same model invocation  
3. Same model invocation → same image  
4. No randomness in any stage  
5. No external factors influencing output

This ensures the system behaves like a **renderer**, not a generative artist.

---

## 8. Extensibility  
Future rendering extensions may include:

- seasonal colour palettes  
- star density mapping  
- moon glow intensity  
- cloud type variation  
- horizon visibility rules  
- custom LoRA for consistent style

Extensions must be:

- deterministic  
- versioned  
- backward‑compatible with DSL v1.0

For roadmap details:  
- roadmap

---

## 9. Summary  
The rendering pipeline is a deterministic interpreter of the scene DSL.  
It transforms symbolic sky state into a minimal, consistent image using a tiny model.  
This separation of DSL → prompt → render ensures clarity, stability, and extensibility across future versions.

---

