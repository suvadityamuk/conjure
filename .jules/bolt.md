## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-18 - Client Instantiation Overhead
**Learning:** `google.genai.Client` instantiation incurs significant overhead (~350ms per call) in this environment. Instantiating it multiple times per pipeline execution (1 for prompt refinement, 4 for image generation) results in ~1.4s of unnecessary delay.
**Action:** Always follow dependency injection patterns for API clients, instantiating them once per pipeline run and passing the instance to utility functions, avoiding repeated instantiation.
