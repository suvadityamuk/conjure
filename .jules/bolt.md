## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-24 - [Eliminate Gemini Client Overhead via Dependency Injection]
**Learning:** Repeatedly instantiating `google.genai.Client` with an API key inside utility functions incurs a ~100ms overhead per call, which adds up during tasks requiring multiple API interactions.
**Action:** Initialize the `Client` once per task lifecycle in the parent process and pass the object directly to utility functions (dependency injection) to avoid redundant instantiations and save execution time.
