bl_info = {
    "name": "Conjure 3D AI",
    "author": "Suvaditya Mukherjee",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > N-Panel > Conjure",
    "description": "Generate 3D objects from text using Gemini and Meshy",
    "category": "3D View",
}

from . import properties
from . import preferences
from . import operators
from . import panels


def register():
    preferences.register()
    properties.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()
    preferences.unregister()


if __name__ == "__main__":
    register()
