import bpy


class ConjureLogItem(bpy.types.PropertyGroup):
    message: bpy.props.StringProperty()
    type: bpy.props.StringProperty(default="INFO")
    path: bpy.props.StringProperty()


class ConjureSettings(bpy.types.PropertyGroup):
    prompt: bpy.props.StringProperty(
        name="Prompt", default="A futuristic cyberpunk helmet"
    )
    refined_prompt: bpy.props.StringProperty()
    is_running: bpy.props.BoolProperty(default=False)
    show_refined: bpy.props.BoolProperty(default=False)
    logs: bpy.props.CollectionProperty(type=ConjureLogItem)


def register():
    bpy.utils.register_class(ConjureLogItem)
    bpy.utils.register_class(ConjureSettings)
    bpy.types.Scene.conjure = bpy.props.PointerProperty(type=ConjureSettings)


def unregister():
    del bpy.types.Scene.conjure
    bpy.utils.unregister_class(ConjureSettings)
    bpy.utils.unregister_class(ConjureLogItem)
