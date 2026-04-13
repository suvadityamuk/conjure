## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [google.genai.Client Instantiation Overhead]
**Learning:** Instantiating `google.genai.Client` in this application incurs an unexpected ~100ms overhead. Creating it repeatedly inside small utility functions (`refine_prompt`, `generate_image`) adds noticeable lag to a multi-step generation pipeline.
**Action:** Use dependency injection. Create the client once at the pipeline's root (`operators.py`) and pass the `client` object down to the utility functions instead of passing an `api_key` string.
