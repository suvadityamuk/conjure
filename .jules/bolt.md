## 2024-03-21 - [Blender Modal Redraw Optimization]
**Learning:** Blender modal operators running on timers can cause significant performance drain if they trigger UI redraws (`area.tag_redraw()`) on every tick, even when no state has changed.
**Action:** Always implement a "dirty flag" (e.g., `state_changed`) in modal loops to conditionally trigger redraws only when necessary updates have occurred.
