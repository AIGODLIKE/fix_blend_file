from . import reg

bl_info = {
    "name": "Fix Blend File",
    "description": "Repair Blend files, some of the files open Blend will flash back, you can use this plug-in repair",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "Top toolbar and bottom of preferences",
    "category": "幻之境",
    "author": "AIGODLIKE Community(小萌新)",
}


def register():
    reg.register()


def unregister():
    reg.unregister()
