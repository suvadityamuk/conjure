## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Instantiation Bottleneck]
**Learning:** `google.genai.Client` instantiation is an expensive operation (~350ms overhead) and should not be invoked multiple times per API call, particularly in iterative or nested workflows like multi-view generation.
**Action:** When a sequence of operations requires making API calls to the same service provider, instantiate the client object once via dependency injection at the highest scope, and pass the object down through the helper functions.
