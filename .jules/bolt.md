## 2026-01-19 - [Blender Modal Operator Redraws]
**Learning:** Blender `modal` operators running on a timer often trigger `tag_redraw()` unconditionally to update the UI. This forces the viewport to re-render even when nothing changed, wasting CPU/GPU cycles.
**Action:** Always track state changes (e.g., `has_updates`) in the modal loop and only call `tag_redraw()` if a change actually occurred.
