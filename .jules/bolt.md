## 2026-01-20 - [Blender Modal Redraw Optimization]
**Learning:** Blender modal operators running on timers can cause significant performance overhead if they trigger UI redraws (`area.tag_redraw()`) in every execution step, even when idle.
**Action:** Always check if state has actually changed (e.g., using a dirty flag) before calling `tag_redraw()` in a modal loop.
