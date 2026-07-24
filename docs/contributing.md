# Contributing Guide

## 1. Purpose  
This document explains how to contribute to Dynamic Sky Wallpaper.  
The project is structured as a **telemetry → DSL → render** pipeline, and contributions must respect this separation of concerns.

---

## 2. Project Structure  
All code lives under `src/`:

```
src/
│
├── api/            # Telemetry (raw data only)
├── scene/          # Interpretation + DSL construction
├── model/          # Prompt + rendering
├── wallpaper/      # OS integration
└── main.py         # Pipeline orchestration
```

Documentation lives under `docs/`.

---

## 3. Contribution Principles

### 3.1 Determinism  
The system is a digital twin.  
Contributions must preserve:

- deterministic behaviour  
- stable DSL semantics  
- stable prompt generation  
- reproducible rendering  

### 3.2 Separation of Concerns  
Each layer has a strict responsibility:

- **Telemetry**: raw data only  
- **Scene rules**: symbolic interpretation  
- **DSL**: structured sky description  
- **Prompt**: deterministic text  
- **Renderer**: deterministic image  
- **Wallpaper**: OS integration  

Do not mix responsibilities across layers.

### 3.3 Backward Compatibility  
Changes must not break:

- DSL v1.0  
- existing renderers  
- existing config files  

New DSL fields must be optional.

---

## 4. How to Add or Modify Telemetry (`src/api/`)

Telemetry modules must:

- return raw numeric/categorical values  
- avoid symbolic interpretation  
- fail gracefully  
- never produce DSL fields  

If adding a new telemetry source:

1. Create a new module under `src/api/`.  
2. Return raw values in a dictionary.  
3. Document the new fields in `docs/telemetry.md`.  
4. Update `scene/builder.py` to consume the new data.

For deeper guidance:  
- telemetry

---

## 5. How to Extend the Scene DSL (`docs/dsl-spec.md`)

To add a new DSL field:

1. Add the field to the DSL spec.  
2. Define its domain (enum, boolean, numeric).  
3. Define its semantics.  
4. Add interpretation logic in `scene/rules.py`.  
5. Add the field to `scene/builder.py`.  
6. Update prompt generation rules.  
7. Ensure renderers ignore unknown fields gracefully.

DSL changes must follow versioning rules:  
- new fields optional  
- no semantic changes to existing fields  
- no breaking changes without version bump

For deeper guidance:  
- scene DSL

---

## 6. How to Modify Scene Rules (`src/scene/rules.py`)

Rules convert raw telemetry → symbolic categories.

Rules must be:

- deterministic  
- pure functions  
- free of side effects  
- independent of rendering logic  

If adding a new rule:

- ensure it maps raw telemetry to a symbolic category  
- update the DSL spec  
- update the builder  
- add tests

For deeper guidance:  
- rule engine

---

## 7. How to Modify Prompt Generation (`src/model/prompt.py`)

Prompt generation must remain:

- deterministic  
- one‑to‑one with DSL fields  
- free of stylistic variation  
- free of randomness  
- free of synonyms  

If adding a new DSL field:

- add a new line to the prompt  
- keep phrasing minimal and declarative  
- avoid creative language

---

## 8. How to Modify Rendering (`src/model/render.py`)

Rendering must:

- use deterministic settings  
- produce identical output for identical prompts  
- avoid randomness  
- avoid stylistic drift  
- avoid external dependencies beyond the model  

If adding rendering features:

- ensure they are deterministic  
- ensure they are controlled by DSL fields  
- update `docs/rendering.md`

For deeper guidance:  
- renderer design

---

## 9. How to Modify Wallpaper Integration (`src/wallpaper/`)

Wallpaper modules must:

- accept a file path  
- apply the wallpaper deterministically  
- isolate OS‑specific logic  
- fail gracefully  

If adding support for a new OS:

- create a new module  
- update the orchestrator  
- document behaviour in `docs/architecture.md`

---

## 10. Testing (`tests/`)

Tests should cover:

- DSL rule functions  
- prompt generation  
- renderer determinism  
- telemetry parsing  
- config loading  

Tests must not rely on external APIs.

---

## 11. Code Style

- Python 3.10+  
- PEP8 formatting  
- Pure functions where possible  
- No global state  
- No side effects in rules or prompt generation  
- Clear naming aligned with DSL semantics  

---

## 12. Opening Pull Requests

PRs must include:

- description of changes  
- justification  
- updated documentation  
- tests for new logic  
- confirmation of deterministic behaviour  

---

## 13. Summary  
Contributions must preserve the system’s core identity:

- **telemetry → DSL → render**  
- deterministic  
- symbolic  
- modular  
- extensible  

This ensures the project remains a clean, minimal digital‑twin engine.

---

