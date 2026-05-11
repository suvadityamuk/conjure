## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-21 - [Gemini Client Instantiation Overhead]
**Learning:** Instantiating `google.genai.Client` is an expensive operation (taking ~100ms) because it validates credentials and sets up connections. Calling `Client(api_key)` inside frequently used utility functions causes unnecessary, repeated overhead.
**Action:** Use dependency injection. Instantiate the `Client` once at the start of a process (e.g., in the operator's background thread) and pass the `client` object to utility functions instead of an API key string.
