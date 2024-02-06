
# development

# from kivy.factory import Factory
# from kaki.app import App

# deployment
from android.permissions import request_permissions, Permission

# deployment
from kivymd.app import MDApp
from app_files.templates import EntryPoint
from kivy.lang.builder import Builder

Builder.load_file("kivy_files/components.kv")
Builder.load_file("kivy_files/kivy_lang.kv")
request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
class HotReload(MDApp):
    #development

    # CLASSES={'EntryPoint':'app_files.templates'}
    # KV_FILES=["kivy_files/components.kv",'kivy_files/kivy_lang.kv']
    # AUTORELOADER_PATHS=[('app_files',{'recursive':True}),('kivy_files',{'recursive':True})]
    # def build_app(self):
    #     return Factory.EntryPoint()

    # deployment
    def build(self):
        return EntryPoint()

if __name__=='__main__':
    HotReload().run()
