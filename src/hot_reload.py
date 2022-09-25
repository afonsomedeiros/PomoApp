from kivy.lang import Builder
from kivymd.tools.hotreload.app import MDApp


class HotReload(MDApp):
    title = "Pomodoro"
    KV_FILES: str = ['pomodoro.kv']
    DEBUG: bool = True

    def build_app(self):
        return Builder.load_file("pomodoro.kv")


HotReload().run()
