from kivy.factory import Factory
from kaki.app import App
from kivymd.app import MDApp


class HotReload(App,MDApp):
    CLASSES={'EntryPoint':'app_folder.main_ui'}
    KV_FILES=['app_folder/kivy_lang.kv','app_folder/components.kv']
    AUTORELOADER_PATHS=[('.',{'recursive':True})]
    def build_app(self):
        return Factory.EntryPoint()

if __name__=='__main__':
    HotReload().run()
