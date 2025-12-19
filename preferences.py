import bpy
import sys
import subprocess


class ConjurePreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    gemini_api_key: bpy.props.StringProperty(
        name="Gemini API Key",
        subtype='PASSWORD'
    )
    meshy_api_key: bpy.props.StringProperty(
        name="Meshy API Key",
        subtype='PASSWORD'
    )
    deps_installed: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="API Keys")
        box.prop(self, "gemini_api_key")
        box.prop(self, "meshy_api_key")
        
        box = layout.box()
        box.label(text="Dependencies")
        row = box.row()
        if self.deps_installed:
            row.label(text="Installed", icon='CHECKMARK')
        else:
            row.label(text="google-genai, requests, pillow", icon='INFO')
        row.operator("conjure.install_deps", text="Install" if not self.deps_installed else "Reinstall")


class CONJURE_OT_InstallDeps(bpy.types.Operator):
    bl_idname = "conjure.install_deps"
    bl_label = "Install Dependencies"

    def execute(self, context):
        python = sys.executable
        packages = ["google-genai", "requests", "pillow"]
        
        try:
            subprocess.check_call([python, "-m", "ensurepip"])
        except:
            pass
        
        try:
            subprocess.check_call([python, "-m", "pip", "install"] + packages)
            context.preferences.addons[__package__].preferences.deps_installed = True
            self.report({'INFO'}, "Dependencies installed!")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CONJURE_OT_InstallDeps)
    bpy.utils.register_class(ConjurePreferences)


def unregister():
    bpy.utils.unregister_class(ConjurePreferences)
    bpy.utils.unregister_class(CONJURE_OT_InstallDeps)
