## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [API Client Overhead]
**Learning:** Instantiating `google.genai.Client` repeatedly incurs an overhead of ~75ms per call. When making multiple successive API calls (like refining a prompt and then generating multiple views), this delay accumulates.
**Action:** Use dependency injection to instantiate the API client once at the pipeline level and pass it down to utility functions to reuse the existing connection/instance.
