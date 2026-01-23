## 2024-10-12 - Blender Modal Operator Performance
**Learning:** Blender modal operators running on timers often default to calling `area.tag_redraw()` on every pass to ensure UI responsiveness. However, this causes continuous full viewport rendering even when nothing changes, leading to high GPU/CPU usage during background tasks.
**Action:** Always track state changes or message queue processing in modal operators and only call `tag_redraw()` when an actual UI update is required.
