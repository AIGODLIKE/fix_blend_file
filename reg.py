from . import (
    ui,
    ui_list,

    ops,
    properties,
    preferences,
    translate
)

module_list = [
    ui,
    ui_list,

    ops,
    properties,
    preferences,
    translate
]


def register():
    for mod in module_list:
        mod.register()


def unregister():
    for mod in module_list[::-1]:
        mod.unregister()
