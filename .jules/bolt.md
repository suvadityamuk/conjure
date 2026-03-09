## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-23 - [Gemini Client Overhead]
**Learning:** Instantiating `google.genai.Client` with an API key incurs a notable overhead (~75ms per instantiation). Creating multiple instances during a single request pipeline creates unnecessary delays.
**Action:** Instantiate the client once at the beginning of the pipeline and use dependency injection to pass the client object to downstream utility functions instead of re-instantiating it with the raw API key.
