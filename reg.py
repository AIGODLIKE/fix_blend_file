from . import (
    ui,
    ui_list,

    ops,
    properties,
    preferences
)

module_list = [
    ui,
    ui_list,

    ops,
    properties,
    preferences
]


def register():
    for mod in module_list:
        mod.register()


def unregister():
    for mod in module_list[::-1]:
        mod.unregister()
