import random

from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget

Window.size = (480, 853)


class FieldWidget(Widget):
    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        with self.canvas:
            # for y in range(0, 100, 17):
            # Сайз хинты не работают кста
            for y in range(0, 3 * Window.size[1] // 4, Window.size[1] // 7):
                Color(0, 1, 0)
                # Ellipse(pos_hint={'x': 0, 'y': y / 100.0}, size_hint=(0.04, 0.04))
                Ellipse(pos=(0, y), size_hint=(0.04, 0.04))
                Color(1, 1, 0)
                # Ellipse(pos_hint={'x': 0.33, 'y': y / 100.0}, size_hint=(0.04, 0.04))
                Ellipse(pos=(Window.size[0] // 4, y), size_hint=(0.04, 0.04))
                Color(0, 0, 1)
                # Ellipse(pos_hint={'x': 0.67, 'y': y / 100.0}, size_hint=(0.04, 0.04))
                Ellipse(pos=(2 * Window.size[0] // 4, y), size_hint=(0.04, 0.04))
                Color(1, 0, 0)
                # Ellipse(pos_hint={'x': 1, 'y': y / 100.0}, size_hint=(0.04, 0.04))
                Ellipse(pos=(3 * Window.size[0] // 4, y), size_hint=(0.04, 0.04))


class RouletteWidget(Widget):
    def __init__(self, **kwargs):
        super(RouletteWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 0, 0, 1)
            self.roulette = Ellipse(pos=(Window.size[0] - 100, Window.size[1] - 100), size=(200, 200))

    def change_color(self):
        c = self.canvas
        c.clear()
        with c:
            Color(rgba=random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]))
            self.roulette = Ellipse(pos=(Window.size[0] - 100, Window.size[1] - 100), size=(200, 200))


class MoveTimer(Label):
    a = NumericProperty(10)
    players = NumericProperty(3)

    def start(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a)

        def finish_callback(*args):
            roulette.change_color()
            i = int(player_move.text[-1])
            if i == self.players:  # and player 1,2,3 or who did not lose
                player_move.text = "Player №1"
            else:
                player_move.text = "Player №" + str(i + 1)
            self.anim = Animation(a=0, duration=self.a)

        self.anim.repeat = True  # ne rabotaet
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = str(round(value, 1)) + " seconds"


timer = MoveTimer()
roulette = RouletteWidget()
player_move = Label(text="Player №..")


class TwisterApp(App):

    def btn(*args):
        show_popup()

    def build(self):
        screen = BoxLayout(orientation="vertical")
        info = BoxLayout(orientation="horizontal", size_hint_y=0.125)
        move = BoxLayout(orientation="vertical")
        move.add_widget(timer)
        move.add_widget(player_move)
        info.add_widget(move)
        settings = Button(background_normal="settings.png", background_down="settingsdown.png")
        settings.bind(on_press=self.btn)
        info.add_widget(settings)
        info.add_widget(roulette)
        screen.add_widget(info)
        field = FieldWidget(size_hint_y=0.875)
        screen.add_widget(field)
        return screen


def show_popup():
    content = GridLayout(cols=3)
    content.add_widget(Label(text="Players"))
    players_label = Label(text="3")
    players_slider = Slider(min=1, max=5, value=3, step=1)
    content.add_widget(players_label)
    content.add_widget(players_slider)
    content.add_widget(Label(text="Fingers"))
    fingers_label = Label(text="3")
    fingers_slider = Slider(min=1, max=5, value=3, step=1)
    content.add_widget(fingers_label)
    content.add_widget(fingers_slider)
    content.add_widget(Label(text="Time for move"))
    time_label = Label(text="10")
    time_slider = Slider(min=5, max=15, value=10, step=5)
    content.add_widget(time_label)
    content.add_widget(time_slider)

    def OnPSliderValueChange(instance, value):
        players_label.text = str(value)

    def OnFSliderValueChange(instance, value):
        fingers_label.text = str(value)

    def OnTSliderValueChange(instance, value):
        time_label.text = str(value)

    players_slider.bind(value=OnPSliderValueChange)
    fingers_slider.bind(value=OnFSliderValueChange)
    time_slider.bind(value=OnTSliderValueChange)

    content.add_widget(Widget())
    content.add_widget(Widget())
    ok = Button(text="Ok")
    content.add_widget(ok)
    popup = Popup(title='Game settings', content=content, auto_dismiss=False)
    ok.bind(on_press=popup.dismiss)

    def change_values(instance):
        timer.a = time_slider.value
        timer.players = players_slider.value
        timer.start()
        player_move.text = "Player №1"

    popup.bind(on_dismiss=change_values)
    popup.open()


if __name__ == "__main__":
    TwisterApp().run()
