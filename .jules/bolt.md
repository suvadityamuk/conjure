## 2024-05-21 - [Blender Modal Redraws]
**Learning:** Blender `modal` operators run frequently (e.g. every 0.3s). Calling `area.tag_redraw()` unconditionally in the loop forces constant viewport rendering, even when no state has changed, causing unnecessary CPU/GPU load.
**Action:** Only call `tag_redraw()` when the operator actually processes data or updates the UI state (e.g., via a `refresh_needed` flag).

## 2024-05-22 - [Avoid Repeated Instantiation of API Clients]
**Learning:** Instantiating the `google.genai.Client` has a noticeable overhead (~200-350ms per instance). Creating it inside utility functions that are called repeatedly (e.g., in a loop or parallel execution for multi-view generation) compounds this latency, causing unnecessary delays.
**Action:** Use dependency injection. Instantiate the client once at a higher level (e.g., at the start of the pipeline) and pass the instantiated client object directly into utility functions to reuse the existing connection.
