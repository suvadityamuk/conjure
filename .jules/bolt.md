## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-06-25 - [Gemini Client Instantiation Overhead]
**Learning:** `google.genai.Client` instantiation incurs significant overhead (~100ms per instantiation). Creating it repeatedly inside helper functions for multiple operations (e.g., prompt refinement, then 4 image generations) multiplies this overhead unnecessarily.
**Action:** Instantiate API clients once per request lifecycle or pipeline run and pass the client instance via dependency injection to helper functions, rather than passing the raw API key and re-instantiating.
