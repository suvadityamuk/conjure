## 2024-05-23 - Blender Modal Operator Redraws
**Learning:** Blender modal operators executing on timer events should only call `area.tag_redraw()` when state actually changes (e.g. a message was processed from the queue) to avoid high CPU/GPU usage from unnecessary viewport rendering.
**Action:** Always check for state changes before calling `tag_redraw()` in modal operators.
