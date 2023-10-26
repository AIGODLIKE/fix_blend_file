import os.path

import bpy.utils
from bpy.types import AddonPreferences


class FixPreferences(AddonPreferences):
    bl_idname = os.path.basename(os.path.dirname(__file__))

    def draw(self, context):
        from .ui import show_fix_ui_button
        show_fix_ui_button(self.layout)


def register():
    bpy.utils.register_class(FixPreferences)


def unregister():
    bpy.utils.unregister_class(FixPreferences)
