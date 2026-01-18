## 2024-05-23 - [Blender Modal Operator Redraws]
**Learning:** Blender modal operators running on a timer event (e.g., every 0.3s) can cause significant performance overhead if they unconditionally call `area.tag_redraw()` even when no state has changed.
**Action:** Always track state changes within the modal loop and conditionally call `tag_redraw()` only when necessary to update the UI.
