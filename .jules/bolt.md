## 2024-05-22 - [Unnecessary Viewport Redraws in Modal Operators]
**Learning:** Blender modal operators running on a timer often trigger `area.tag_redraw()` indiscriminately. In `conjure`, this caused continuous viewport updates even when the generation queue was empty, wasting CPU/GPU resources.
**Action:** Always implement a `needs_redraw` flag in modal loops to ensure `tag_redraw()` is only called when state actually changes.
