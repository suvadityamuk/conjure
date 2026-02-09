## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-23 - [API Client Overhead]
**Learning:** Instantiating `google.genai.Client` is not cheap (measured ~100ms per call). When making multiple sequential or parallel API calls, re-creating the client inside the loop adds significant cumulative overhead (~500ms for 5 calls).
**Action:** Initialize API clients once at the start of the workflow (e.g. in the operator or main function) and pass the instance to helper functions via dependency injection.
