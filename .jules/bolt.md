## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2026-02-23 - [GenAI Client Overhead]
**Learning:** Instantiating `google.genai.Client` is surprisingly expensive (~80ms). Doing this inside loops or repeatedly inside helper functions can add significant latency (e.g., ~400ms for 5 calls).
**Action:** Always instantiate the client once and pass it down (dependency injection) to helper functions, especially in performance-critical loops or multi-step pipelines.
