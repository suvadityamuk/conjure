## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2026-02-16 - [API Client Overhead]
**Learning:** `google.genai.Client` initialization has a measurable overhead (~75-100ms). Reusing the client instance across sequential and parallel requests saves ~400ms in a multi-step generation pipeline.
**Action:** Always instantiate API clients once at the beginning of a workflow and pass them down, rather than creating them inside helper functions.
