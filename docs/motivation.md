# Motivation

## 1. Purpose  
Dynamic Island Wallpaper exists to solve a specific cognitive problem: **timeblindness during deep work**.  
When fully absorbed in a task, environmental context fades — hours pass unnoticed, daylight disappears, weather changes, and the outside world shifts without registering.  
This project provides a **non‑intrusive, ambient cue system** that restores situational awareness without breaking focus.

---

## 2. The Problem: Timeblindness  
Timeblindness is not simply “forgetting the time.”  
It is losing *context*:

- daylight fades without noticing  
- weather changes without registering  
- dusk becomes night without awareness  
- long work sessions stretch far past healthy hours  

Traditional solutions — alarms, notifications, reminders — are intrusive and break flow.  
What’s needed is a **passive, continuous environmental indicator**.

---

## 3. The Solution: Ambient Environmental Cues  
Dynamic Island Wallpaper externalises real‑world conditions into a **symbolic island scene** using the scene DSL.  
This symbolic state is rendered into a minimalist wallpaper that updates quietly every few minutes.

It provides:

- **light level cues** → macro sense of time  
- **sun position** → direction + progression  
- **sky mode** → dawn/day/dusk/night as a visual clock  
- **weather state** → BOM‑derived conditions  
- **tide height** → slow environmental rhythm  
- **wind + waves** → motion cues  
- **moon visibility** → late‑night indicator  
- **daily‑rhythm animations** → morning, work, breaks, evening, sleep  

These cues sit in peripheral vision, gently signalling environmental change.

---

## 4. Why a DSL?  
The DSL is the core innovation.  
It compresses real telemetry into a **stable symbolic snapshot**:

- deterministic  
- minimal  
- renderer‑agnostic  
- easy to extend  
- cognitively meaningful  

The DSL ensures the wallpaper is not “artistic noise” but a **functional environmental indicator**.

For details:  
- DSL spec  
- rule engine

---

## 5. Why a Deterministic Semantic Layer?  
The system is built around **deterministic semantics**:

- BOM + astronomy telemetry → deterministic numeric facts  
- Prolog → deterministic symbolic bucketing  
- DSL → deterministic symbolic scene  

Determinism is binary — **a pipeline is deterministic or it is not**.

### Procedural Rendering (Deterministic)  
The procedural compositor produces:

> **Same DSL + same base image → same PNG, byte‑for‑byte.**

This mode is ideal for stability, reproducibility, and long‑term consistency.

### Generative Rendering (Non‑Deterministic)  
If a generative transformation (e.g., img2img) is applied to a reference image:

> **The output is not deterministic**, even with fixed seeds.

This mode is optional and explicitly non‑deterministic.

---

## 6. Why This Matters  
This project is a cognitive prosthetic.  
It helps maintain:

- temporal awareness  
- environmental awareness  
- healthy work rhythms  
- connection to the outside world  

All without notifications, interruptions, or alarms.

It is a **quiet companion** for deep work.

---

## 7. Long‑Term Motivation  
The island twin is the first domain.  
The broader motivation is to build a general **ambient digital‑twin framework** that supports:

- city activity  
- personal activity  
- ocean/tide states  
- network flow  
- environmental rhythm  

For future expansion:  
- multi‑domain twin engine

---

## 8. Summary  
Dynamic Island Wallpaper exists to gently anchor you in time and environment while you work.  
It restores context through ambient cues, using a symbolic DSL and a deterministic semantic pipeline to create a stable, meaningful visual companion — with optional generative rendering when stylistic variation is desired.

---

