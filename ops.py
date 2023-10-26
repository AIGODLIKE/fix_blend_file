import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator


def clear_list():
    from .properties import types, prefix

    for t in types:
        getattr(bpy.context.scene, f'{prefix}{t}').clear()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')


class SwitchFixUi(Operator):
    bl_label = '弹出修复窗口'
    bl_idname = 'wm.popup_fix_blend_window'
    bl_description = '弹出修复Blend文件窗口'

    popup_window: BoolProperty(default=False, name='弹出窗口',
                               options={'SKIP_SAVE'})

    def execute(self, context):
        if self.popup_window:
            bpy.ops.screen.userpref_show()
        from . import ui
        ui.SwitchPropertyUi.switch()
        self.show_header(context)
        context.preferences.active_section = 'ADDONS'
        bpy.ops.wm.redraw_timer(type='DRAW_WIN')
        return {'FINISHED'}

    @staticmethod
    def show_header(context: "bpy.types.Context"):
        def set_header(areas: list[bpy.types.Area]):
            for area in areas:
                if area.type == 'PREFERENCES':
                    area.spaces[0].show_region_header = True

        for win in context.window_manager.windows:
            set_header(win.screen.areas)


class LoadFile:
    bl_idname: str

    # report: "function"
    # ops: "function"

    def execute(self, context):
        print(self, dir(self))
        getattr(self, 'before_func', lambda: print('before'))()

        from .properties import types
        path = context.scene.fix_blend_file_path
        try:
            with bpy.data.libraries.load(path) as (data_from, data_to):
                '''查找是否有匹配的集合'''
                for t in types:
                    self.ops(data_from, data_to, t)
                self.data_from = data_from
                self.data_to = data_to
        except Exception as e:
            self.report({'ERROR'}, '加载文件错误,请选择Blender文件' + str(e.args))
        getattr(self, 'after_func', lambda: print('after'))()
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')
        return {"FINISHED"}


class LoadFixFileData(Operator, LoadFile):
    bl_label = '加载数据'
    bl_idname = 'fix.load_fix_file_data'
    bl_description = '加载需要修复的文件数据'

    def ops(self, data_from, data_to, t):
        from .properties import prefix
        prop = getattr(bpy.context.scene, f'{prefix}{t}')
        for i in getattr(data_from, t.lower()):
            a = prop.add()
            a.name = i

    def before_func(self):
        clear_list()


class ImportErrorFileData(Operator, LoadFile):
    bl_label = '导入数据'
    bl_idname = 'fix.import_error_file_data'
    bl_description = "导入错误文件的数据"
    type: StringProperty()
    import_list = []

    def ops(self, data_from, data_to, t):
        from .properties import prefix
        if self.type == t:
            prop = getattr(bpy.context.scene, f'{prefix}{t}')

            # 拿到选中了的项的名称
            selected_list = list(map(lambda f: f.name, filter(lambda j: j.selected, prop.values())))

            data_t = getattr(data_to, t.lower())

            # 如果导入的文件里面有那个名称的东东就导入一下
            for i in getattr(data_from, t.lower()):
                if i in selected_list:
                    data_t.append(i)
                    print('导入了这个', t, i)

    def after_func(self):
        if getattr(self, 'import_list', False):
            print(self.import_list)
            print('self.data_to', self.data_to)
            print('self.data_from', self.data_from)


class SelectedSwitch(Operator):
    bl_label = '切换选择'
    bl_idname = 'fix.selected_switch'
    bl_description = "切换全选或者取消全选"
    type: StringProperty()

    def execute(self, context):
        from .properties import prefix
        col = getattr(bpy.context.scene, f'{prefix}{self.type}')
        if len(col):
            b = col[0].selected
            for i in col.values():
                i.selected = b ^ True
        else:
            self.report({'INFO'}, f'未找到项{self.type}')
        return {"FINISHED"}


class ClearFixList(Operator):
    bl_label = '清理列表'
    bl_idname = 'fix.clear_list'
    bl_description = "清理修复的列表"

    def execute(self, context):
        clear_list()
        return {"FINISHED"}


class_list = [
    SwitchFixUi,
    LoadFixFileData,
    ImportErrorFileData,
    SelectedSwitch,
    ClearFixList
]
reg, unreg = bpy.utils.register_classes_factory(class_list)


def register():
    reg()


def unregister():
    unreg()
