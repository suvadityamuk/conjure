## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Gemini Client Instantiation Overhead]
**Learning:** Instantiating `google.genai.Client` and dynamically importing its dependencies inside repeated functions (like `generate_image`) incurs a ~75ms overhead per call. In pipelines generating multiple images, this accumulates to a measurable delay (~300-400ms).
**Action:** Instantiate the `Client` once at the beginning of the pipeline and pass it (dependency injection) to utility functions. Keep imports at the module level when possible.
