## 2026-01-17 - Blender Modal Operator Redraws
**Learning:** Blender modal operators with timers (e.g. checking a queue) can cause severe performance issues if they call `area.tag_redraw()` on every tick. This forces the entire 3D viewport to re-render even when idle.
**Action:** Always use a state tracking flag (e.g. `updated = True`) inside the message processing loop. Only call `tag_redraw()` if `updated` is True.
