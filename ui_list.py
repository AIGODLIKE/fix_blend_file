import bpy.utils
from bpy.types import UIList
from .properties import types


class DrawFixItems(UIList):
    bl_idname = "UI_LIST_UL_FIX_BLEND_FILE"

    def draw_item(self,
                  context: 'bpy.context',
                  layout: 'bpy.types.UILayout',
                  data: 'AnyType',
                  item: 'AnyType',
                  icon: int,
                  active_data: 'AnyType',
                  active_property: str,
                  index: int = 0,
                  flt_flag: int = 0):
        row = layout.row(align=True)
        row.label(text=item.name, translate=False)
        row.separator_spacer()
        row.separator_spacer()
        row.separator_spacer()
        row.prop(
            item,
            'selected',
            text="",
            icon="RESTRICT_SELECT_OFF" if item.selected else "RESTRICT_SELECT_ON"
        )


reg_list = []


def register():
    for t in types:
        c = type('emm', (DrawFixItems,), {})
        c.bl_idname += t.upper()
        bpy.utils.register_class(c)
        reg_list.append(c)


def unregister():
    for c in reg_list:
        bpy.utils.unregister_class(c)
    reg_list.clear()
