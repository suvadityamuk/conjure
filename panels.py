import bpy
import os


class CONJURE_PT_Main(bpy.types.Panel):
    bl_label = "Conjure"
    bl_idname = "CONJURE_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Conjure'

    def draw(self, context):
        layout = self.layout
        tool = context.scene.conjure
        prefs = context.preferences.addons.get(__package__)
        
        # Check for API keys
        if not prefs or not prefs.preferences.gemini_api_key or not prefs.preferences.meshy_api_key:
            box = layout.box()
            box.label(text="API Keys Required", icon='ERROR')
            box.label(text="Edit > Preferences > Add-ons > Conjure")
            return
        
        # Prompt input
        layout.prop(tool, "prompt", text="")
        
        # Generate button
        row = layout.row()
        row.scale_y = 1.5
        row.enabled = not tool.is_running
        if tool.is_running:
            row.operator("conjure.generate_all", text="Generating...", icon='TIME')
        else:
            row.operator("conjure.generate_all", text="Generate 3D", icon='PLAY')
        
        # Logs
        if tool.logs:
            box = layout.box()
            box.label(text="Progress")
            for log in reversed(list(tool.logs)[-8:]):
                row = box.row()
                icon = 'IMAGE_DATA' if log.type == 'IMAGE' else 'INFO'
                row.label(text=log.message, icon=icon)
                if log.path and os.path.exists(log.path):
                    op = row.operator("wm.url_open", text="", icon='FILE_FOLDER')
                    op.url = f"file://{log.path}"
        
        # Refined prompt (expandable)
        if tool.refined_prompt:
            box = layout.box()
            row = box.row()
            row.prop(tool, "show_refined", icon='TRIA_DOWN' if tool.show_refined else 'TRIA_RIGHT', 
                     text="Refined Prompt", emboss=False)
            if tool.show_refined:
                col = box.column()
                # Word wrap the text
                self._draw_wrapped_text(col, tool.refined_prompt, width=35)
    
    def _draw_wrapped_text(self, layout, text, width=40):
        """Draw text with word wrapping."""
        words = text.split()
        line = ""
        for word in words:
            if len(line) + len(word) + 1 > width:
                layout.label(text=line)
                line = word
            else:
                line = f"{line} {word}".strip()
        if line:
            layout.label(text=line)


def register():
    bpy.utils.register_class(CONJURE_PT_Main)


def unregister():
    bpy.utils.unregister_class(CONJURE_PT_Main)
