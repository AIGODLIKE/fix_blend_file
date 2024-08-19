import bpy

from .zh_CN import zh_CN


class TranslationHelper:
    def __init__(self, name: str, data: dict, lang='zh_CN'):
        self.name = name
        self.translations_dict = dict()

        for src, src_trans in data.items():
            key = ("Operator", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans
            key = ("*", src)
            self.translations_dict.setdefault(lang, {})[key] = src_trans

    def register(self):
        try:
            bpy.app.translations.register(self.name, self.translations_dict)
        except ValueError:
            pass

    def unregister(self):
        bpy.app.translations.unregister(self.name)


SimpleDeform_CN = TranslationHelper('Fix_Blend_File_CN', zh_CN)
SimpleDeform_HANS = TranslationHelper('Fix_Blend_File_HANS', zh_CN, lang='zh_HANS')


def __ts__(string) -> str:
    from bpy.app.translations import pgettext
    view = bpy.context.preferences.view
    language = view.language
    if language in ('zh_HANS', 'zh_CN') and view.use_translate_interface:
        return pgettext(string)
    return string


def register():
    if bpy.app.version < (4, 0, 0):
        SimpleDeform_CN.register()
    else:
        SimpleDeform_CN.register()
        SimpleDeform_HANS.register()


def unregister():
    if bpy.app.version < (4, 0, 0):
        SimpleDeform_CN.unregister()
    else:
        SimpleDeform_CN.unregister()
        SimpleDeform_HANS.unregister()
