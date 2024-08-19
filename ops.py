import bpy
from bpy.props import BoolProperty, StringProperty
from bpy.types import Operator


def clear_list():
    from .properties import types, prefix

    for t in types:
        getattr(bpy.context.scene, f'{prefix}{t}').clear()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')


class SwitchFixUi(Operator):
    bl_label = 'Popup fix window'
    bl_idname = 'wm.popup_fix_blend_window'
    bl_description = 'Popup fix blend file window'

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
    bl_label = 'Load data'
    bl_idname = 'fix.load_fix_file_data'
    bl_description = 'Load the file data that needs to be fix'

    def ops(self, data_from, data_to, t):
        from .properties import prefix
        prop = getattr(bpy.context.scene, f'{prefix}{t}')
        for i in getattr(data_from, t.lower()):
            a = prop.add()
            a.name = i

    def before_func(self):
        clear_list()


class ImportErrorFileData(Operator, LoadFile):
    bl_label = 'Import data'
    bl_idname = 'fix.import_error_file_data'
    bl_description = "Importing data from error files"
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
        t = self.type.lower()
        items = getattr(self.data_to, t)
        if t == 'objects':
            for o in items:
                bpy.context.collection.objects.link(o)
        elif t == 'collections':
            for c in items:
                bpy.context.collection.children.link(c)

        self.report({'INFO'}, 'Import complete!')

    def link_to_scene(self):
        ...


class SelectedSwitch(Operator):
    bl_label = 'Switch select'
    bl_idname = 'fix.selected_switch'
    bl_description = "Switch all or cancel select"
    type: StringProperty()

    def execute(self, context):
        from .properties import prefix
        col = getattr(bpy.context.scene, f'{prefix}{self.type}')
        if len(col):
            b = col[0].selected
            for i in col.values():
                i.selected = b ^ True
        else:
            from bpy.app.translations import pgettext
            self.report({'INFO'}, f'{pgettext("Not find item")}{self.type}')
        return {"FINISHED"}


class ClearFixList(Operator):
    bl_label = 'Clear list'
    bl_idname = 'fix.clear_list'
    bl_description = "Clear fix list"

    def execute(self, _):
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
