from itertools import cycle

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout


class Cycle:
    def __init__(self):
        self.cycle = cycle([
            Timer(25), Timer(5),
            Timer(25), Timer(5),
            Timer(25), Timer(30)
        ])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.cycle)


class Timer:
    def __init__(self, time):
        self.time = time * 60

    def decrease(self):
        self.time -= 1
        return self.time

    def __str__(self):
        time_info = divmod(self.time, 60)
        return '{:02d}:{:02d}'.format(time_info[0], time_info[1])


class Pomodoro(MDFloatLayout):
    timer_string = StringProperty('25:00')
    button_string = StringProperty("Iniciar!")
    reinitialize_opacity = NumericProperty(0)
    reinitialize_disabled = BooleanProperty(False)
    running = BooleanProperty(False)
    cycle = Cycle()
    clock = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._time = next(self.cycle)
        self.timer_string = str(self._time)

    def start(self):
        self.button_string = "Pausar"
        if not self.running:
            self.running = True
            self.clock = Clock.schedule_interval(self.update, 1)
            self.reinitialize_opacity = 0
            self.reinitialize_disabled = True

    def stop(self):
        self.button_string = "Continuar"
        if self.running:
            self.running = False
            self.clock.cancel()
            self.reinitialize_opacity = 1
            self.reinitialize_disabled = False

    def reinitialize(self):
        self.button_string = "Iniciar"
        self.cycle = Cycle()
        self._time = next(self.cycle)
        self.timer_string = str(self._time)
        self.reinitialize_opacity = 0
        self.reinitialize_disabled = True

    def initial(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def update(self, *args):
        time = self._time.decrease()
        if time == 0:
            self.stop()
            self._time = next(self.cycle)
        self.timer_string = str(self._time)


class PomoApp(MDApp):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DEFAULT_PALETTE = self.theme_cls.primary_palette

    def change_color(self):
        theme = self.theme_cls.theme_style
        if theme == "Light":
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "DeepPurple"
        else:
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = self.DEFAULT_PALETTE

    def build(self):
        return Builder.load_file("pomodoro.kv")
