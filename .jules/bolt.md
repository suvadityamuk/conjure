## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Instantiation]
**Learning:** Instantiating `google.genai.Client` incurs a ~75ms setup overhead per call. Calling this multiple times in a loop or per image view generation adds unnecessary latency.
**Action:** Instantiate the client once in `operators.py` and inject it into utility functions to reuse the instance, saving ~300ms total latency per complete model generation.
