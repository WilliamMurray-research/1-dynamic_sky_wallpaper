# **Dynamic Island Wallpaper: Astronomical Telemetry & Symbolic Sky Projection**  
### Technical Whitepaper v1.0 
---
#### William Murray
#### 26 July 2026
---

## **Abstract**

This document specifies the astronomical telemetry subsystem for *Dynamic Island Wallpaper*, including the computation of solar and lunar apparent positions, lunar phase, twilight classification, and symbolic sky projection. The system converts physically accurate orbital data into deterministic symbolic categories used by the scene DSL and procedural renderer. The design emphasizes correctness, explainability, and architectural simplicity, avoiding full ephemeris implementation while maintaining visually realistic behavior.

---

## **1. Introduction**

The Dynamic Island Wallpaper project renders a digital‑twin sky that reflects real astronomical conditions. The system requires:

- Solar altitude and azimuth  
- Lunar altitude, azimuth, and phase  
- Twilight classification  
- Visibility of stars  
- Symbolic placement of sun and moon in screen space  

The goal is not astrophotography‑grade precision, but **visually correct, deterministic behavior** suitable for symbolic rendering.

The subsystem is rule‑based, with numeric telemetry computed in Python and symbolic classification performed in Prolog.

---

## **2. Coordinate Systems**

### **2.1 Horizontal Coordinate System**

The astronomical engine provides:

- **Altitude (Alt)** — angle above the horizon (0° = horizon, 90° = zenith)  
- **Azimuth (Az)** — compass direction (0° = north, 90° = east, 180° = south, 270° = west)

This coordinate system is ideal for sky rendering because it directly corresponds to human perception.





---

## **3. Orientation Model**

### **3.1 Viewer Orientation**

The island scene assumes the viewer faces **north**.  
Thus:

- **East** should appear on the **right horizon**  
- **West** should appear on the **left horizon**  
- The sun should move **right → left** across the sky (east → west)

### **3.2 Azimuth Rotation**

To achieve this, azimuth is rotated by –90°:

\[
Az_{rot} = (Az - 90) \bmod 360
\]

This produces:

| True Azimuth | Meaning | Rotated Azimuth | Screen Position |
|--------------|---------|------------------|------------------|
| 90° | East | 0° | Right horizon |
| 180° | South | 90° | Lower mid |
| 270° | West | 180° | Left horizon |
| 0° | North | 270° | Upper mid |





---

## **4. Vertical Projection (Altitude → Screen Y)**

Altitude maps linearly to vertical screen position:

\[
y = H \cdot \left(1 - \frac{Alt}{90}\right)
\]

Where:

- `Alt = 0°` → horizon → bottom of screen  
- `Alt = 90°` → zenith → top of screen  

This projection is simple, deterministic, and visually plausible.





---

## **5. Symbolic Bucketing**

The renderer does not use raw `(x, y)` coordinates.  
Instead, Prolog converts them into symbolic categories.

### **5.1 Horizontal Buckets**

Using rotated azimuth:

- `0°–120°` → `"right"`  
- `120°–240°` → `"left"`  
- Else → `"mid"`

### **5.2 Vertical Buckets**

Using altitude:

- `< 15°` → `"bottom"`  
- `15°–45°` → `"mid"`  
- `> 45°` → `"top"`

### **5.3 Combined Sun Position**

\[
sunposition = vert\_bucket + horiz\_bucket
\]

Examples:

- `topright`  
- `midleft`  
- `bottomright`

This symbolic representation is stable across seasons and latitudes.

---

## **6. Solar Height Classification**

Altitude is also bucketed into:

- `none` (sun below horizon)  
- `low`  
- `medium`  
- `high`

These categories drive:

- Sun sprite selection  
- Shadow intensity  
- Palette transitions  

---

## **7. Twilight Model**

Twilight is determined solely by solar altitude:

| Solar Altitude | Mode |
|----------------|------|
| > 6° | day |
| 0°–6° | dusk/dawn |
| –6° to –12° | civil twilight |
| < –12° | night |

This classification drives:

- `sky_mode`  
- `island_palette`  
- star visibility  
- moon visibility  

---

## **8. Lunar Phase Model**

The lunar phase is computed as illumination fraction:

\[
phase \in [0.0, 1.0]
\]

Symbolic buckets:

- `none`  
- `crescent`  
- `half`  
- `gibbous`  
- `full`

Visibility rule:

\[
moon\_visible = (Alt > 0°) \land (sun\_alt < -6°)
\]

---

## **9. Stars Visibility**

Stars are visible when:

- Solar altitude < –6°  
- Weather is not rain or approaching rain  

This produces a boolean `stars` field.

---

## **10. Prolog Rule System**

The Prolog module performs:

1. Azimuth rotation  
2. Horizontal bucketing  
3. Vertical bucketing  
4. Twilight classification  
5. Moon phase bucketing  
6. Stars visibility  
7. DSL JSON assembly  

The rule system is deterministic, monotonic, and explainable.

---

## **11. Determinism & Explainability**

The subsystem is designed to support future “explain‑why” queries:

- *Why is the sky in dusk mode?*  
- *Why is the moon not visible?*  
- *Why is the sun in the top‑right bucket?*

Because all rules are monotonic and threshold‑based, explanations are trivial.

---

## **12. Implementation Summary**

### Python (numeric telemetry)

- Compute sun/moon altitude & azimuth  
- Compute moon phase fraction  
- Emit raw telemetry JSON  

### Prolog (symbolic classification)

- Apply rotation  
- Bucket into symbolic categories  
- Emit DSL JSON  

### Renderer (deterministic compositor)

- Apply overlays based on DSL fields  
- No randomness  
- No generative components unless explicitly enabled  

---

## **13. Future Extensions**

- Seasonal solar path modeling  
- Atmospheric scattering model  
- Star density enum  
- Moon orientation (libration)  
- Smooth interpolation between buckets  
- Multi‑domain sky scenes  

---

## **Conclusion**

This whitepaper defines a complete, deterministic, and explainable astronomical telemetry subsystem suitable for symbolic rendering. The design balances physical realism with architectural simplicity, ensuring that the Dynamic Island Wallpaper remains stable, low‑GPU, and visually coherent across all times of day and seasons.

---


Just tell me which one you want next.
