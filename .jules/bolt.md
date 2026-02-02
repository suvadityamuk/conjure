## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Instantiation Overhead]
**Learning:** Instantiating `google.genai.Client` costs ~80ms-220ms. Instantiating it inside loops or frequently called functions (like `generate_image`) adds up quickly.
**Action:** Instantiate the client once (e.g., in the operator or main thread) and use dependency injection to pass it to utility functions.
