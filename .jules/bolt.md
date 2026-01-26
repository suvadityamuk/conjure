## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Google GenAI Client Reuse]
**Learning:** Creating a new `google.genai.Client()` instance takes ~80ms. The original pipeline created 5 instances sequentially, adding ~400ms overhead. Reusing a single client instance saves this overhead and likely benefits from connection pooling.
**Action:** Instantiate API clients once at the start of a pipeline and pass them down to utility functions using dependency injection.
