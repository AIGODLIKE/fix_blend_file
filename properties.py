import bpy.utils
from bpy.props import BoolProperty, CollectionProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup


class FixItem(PropertyGroup):
    selected: BoolProperty(default=False)
    # name自带


class_list = [
    FixItem,
]

reg, unreg = bpy.utils.register_classes_factory(class_list)

types = ['Scenes', 'Collections', 'Objects', ]
prefix = 'fix_blend_file_'


def register():
    reg()
    for t in types:
        setattr(bpy.types.Scene, f"{prefix}{t}", CollectionProperty(type=FixItem))
        setattr(bpy.types.Scene, f"{prefix}{t}_index", IntProperty())
    bpy.types.Scene.fix_blend_file_path = StringProperty(subtype="FILE_PATH", name="损坏文件路径")


def unregister():
    unreg()
    for t in types:
        delattr(bpy.types.Scene, f"{prefix}{t}")
        delattr(bpy.types.Scene, f"{prefix}{t}_index")

    del bpy.types.Scene.fix_blend_file_path
