## 2025-02-19 - [Blender Modal Operator Redraw]
**Learning:** Blender modal operators running on timers often default to forcing a UI redraw (`tag_redraw()`) on every tick. This is extremely wasteful (CPU/GPU) if the operator is just waiting for a background thread.
**Action:** Always use a flag to track if state actually changed in the `modal` loop, and only call `tag_redraw()` if that flag is set.
