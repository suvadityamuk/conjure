## 2024-05-22 - Blender Modal Operator Redraws
**Learning:** Blender modal operators running on timers often aggressively redraw the 3D Viewport (`area.tag_redraw()`) even when nothing changes, causing high CPU/GPU usage.
**Action:** Always wrap `area.tag_redraw()` in a conditional check that tracks if any state change or UI update actually occurred in the loop.
