## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Overhead]
**Learning:** Instantiating `google.genai.Client` is surprisingly expensive (incurring ~75-80ms overhead per initialization). If recreated across multiple calls or in parallel mapping (like generating multiple views), this creates unnecessary latency.
**Action:** Instantiate the API client once per pipeline/session and pass it via dependency injection to utility functions, rather than passing the API key and creating new client instances inside the utilities.
