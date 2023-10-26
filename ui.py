import bpy


class DrawFixBlendUi:
    layout: 'bpy.types.UILayout'

    # 绘制右边层
    def right_layout(self: bpy.types.Panel, context: bpy.context):
        from .properties import types, prefix
        from .ui_list import DrawFixItems
        from .ops import ImportErrorFileData, SelectedSwitch
        layout = self.layout
        scene = bpy.context.scene

        row = layout.row(align=True)
        for t in types:
            f = f"{prefix}{t}"
            i = f"{prefix}{t}_index"

            column = row.column(align=True)
            column.label(text=t)
            column.template_list(
                DrawFixItems.bl_idname + t.upper(),
                "",
                scene,
                f,
                scene,
                i,
                rows=15,
            )
            r = column.row(align=True)

            r.operator(
                ImportErrorFileData.bl_idname,
                text="导入所选",
                icon="IMPORT"
            ).type = t

            def get_icon():
                items = getattr(context.scene, f, [])
                if len(items):
                    return "RESTRICT_SELECT_ON" if items[0].selected else "RESTRICT_SELECT_OFF"
                else:
                    return "RESTRICT_SELECT_ON"

            r.operator(
                SelectedSwitch.bl_idname,
                text="",
                icon=get_icon()
            ).type = t
        layout.label(text='1.底部选择一个损坏的.blend文件')
        layout.label(text='2.点击加载数据')
        layout.label(text='3.选择任意一种导入选项,然后点击导入所选,将会导入对应的数据到当前工程中')
        layout.separator_spacer()
        layout.label(text='Note:导入集合或物体时需要手动将导入的项添加到场景内,无法自动导入到当前场景!!')

    def left_layout(self: bpy.types.Panel, context: bpy.context):
        column = self.layout.column(align=True)
        from .properties import types, prefix
        from .ops import ClearFixList

        for t in types:
            items = getattr(context.scene, f"{prefix}{t}")
            column.label(text=t)
            box = column.box()
            box.label(text=f'共:{len(items)}')
            box.label(text=f'已选:{len(list(filter(lambda i: i.selected, items)))}')
            column.separator()
            column.separator()
        column.separator_spacer()
        column.separator_spacer()
        column.operator(ClearFixList.bl_idname)

    def bottom_layout(self: bpy.types.Panel, context: bpy.context):
        from .ops import LoadFixFileData

        layout = self.layout
        layout.label(text="损坏文件路径:")
        row = layout.row()
        row.scale_x = 2
        row.prop(bpy.context.scene, 'fix_blend_file_path', text="")
        layout.operator(LoadFixFileData.bl_idname)
        DrawFixBlendUi.exit(self.layout)

    def left_bottom_layout(self: bpy.types.Panel, context: bpy.context):
        DrawFixBlendUi.bottom_layout(self, context)

    @staticmethod
    def exit(layout: 'bpy.types.UILayout') -> 'bpy.types.UILayout.operator':
        """退出按钮
        """
        from .ops import SwitchFixUi
        layout.alert = True
        return layout.operator(SwitchFixUi.bl_idname,
                               text='退出',
                               icon='PANEL_CLOSE'
                               )


class SwitchPropertyUi:
    """设置UI"""
    ui_draw_func = {
        'left': None,
        'right': None,
        'bottom': None,
        'left_button': None,
        'is_overwrite': False,  # 是被替换了的
    }

    @classmethod
    def switch(cls):
        """切换两种状态"""
        is_overwrite = cls.ui_draw_func['is_overwrite']
        if is_overwrite:
            cls.reduction_ui()
        else:
            cls.overwrite_ui()
        cls.refresh_layout()

    @classmethod
    def refresh_layout(cls):
        """刷新界面"""
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')

    @classmethod
    def overwrite_ui(cls):
        """重写ui"""
        data = cls.ui_draw_func
        if not data['is_overwrite']:
            data['is_overwrite'] = True
            data['left'] = bpy.types.USERPREF_PT_navigation_bar.draw
            data['right'] = bpy.types.USERPREF_PT_addons.draw
            data['bottom'] = bpy.types.USERPREF_HT_header.draw
            data['left_button'] = bpy.types.USERPREF_PT_save_preferences.draw
            cls.set_layout_func()

    @classmethod
    def set_layout_func(cls):
        """设置活动Layout的绘制方法"""
        bpy.types.USERPREF_PT_addons.draw = DrawFixBlendUi.right_layout
        bpy.types.USERPREF_PT_navigation_bar.draw = DrawFixBlendUi.left_layout
        bpy.types.USERPREF_HT_header.draw = DrawFixBlendUi.bottom_layout
        bpy.types.USERPREF_PT_save_preferences.draw = DrawFixBlendUi.left_bottom_layout

    @classmethod
    def reduction_ui(cls):
        """还原ui"""
        data = cls.ui_draw_func
        if data['is_overwrite']:
            data['is_overwrite'] = False
            bpy.types.USERPREF_PT_navigation_bar.draw = data['left']
            bpy.types.USERPREF_PT_addons.draw = data['right']
            bpy.types.USERPREF_HT_header.draw = data['bottom']
            bpy.types.USERPREF_PT_save_preferences.draw = data['left_button']


def show_fix_ui_button(lay: "bpy.types.UILayout"):
    from .ops import SwitchFixUi
    lay.operator(SwitchFixUi.bl_idname,
                 icon='FILE_CACHE',
                 text='修复文件',
                 ).popup_window = True
    # emboss=False,


# TOPBAR_MT_file_recover 恢复菜单栏
# 添加按钮到下面的栏用来显示
def draw_switch(self: bpy.types.Panel, context: "bpy.types.Object"):
    layout = self.layout
    region = context.region
    name = self.__class__.__name__

    if name == 'USERPREF_MT_editor_menus':
        show_fix_ui_button(layout)
    elif name == 'USERPREF_PT_save_preferences':
        show_fix_ui_button(layout.row())
    elif name == 'TOPBAR_MT_editor_menus':
        if region.alignment == 'RIGHT':
            ...
        else:
            show_fix_ui_button(layout)


def add_ui():
    bpy.types.TOPBAR_MT_file_recover.append(draw_switch)
    bpy.types.USERPREF_MT_editor_menus.append(draw_switch)
    bpy.types.USERPREF_PT_save_preferences.append(draw_switch)


def del_ui():
    bpy.types.TOPBAR_MT_file_recover.remove(draw_switch)
    bpy.types.USERPREF_MT_editor_menus.remove(draw_switch)
    bpy.types.USERPREF_PT_save_preferences.remove(draw_switch)


def register():
    add_ui()


def unregister():
    del_ui()
