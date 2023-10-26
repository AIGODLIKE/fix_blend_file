from . import reg

bl_info = {
    "name": "Fix Blend File",
    "description": "修复Blend文件,部分文件打开时Blend会闪退,可以使用此插件进行修复",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "顶部工具栏和偏好设置底部",
    "category": "幻之境",
    "author": "AIGODLIKE Community(小萌新)",
}


def register():
    reg.register()


def unregister():
    reg.unregister()
