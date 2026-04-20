## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Instantiation Overhead]
**Learning:** Instantiating the `google.genai.Client` is surprisingly expensive, taking ~100ms per call. In a generation pipeline where multiple image views and prompt refinements are done, this overhead adds up rapidly (e.g. ~500ms for 5 calls).
**Action:** Always instantiate API clients once at the beginning of a pipeline or context and pass them down via dependency injection rather than recreating them in utility functions.
