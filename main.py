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

Window.size = (400, 711)


def define_circle(pos):
    res = []
    if 0 <= pos[1] <= Window.size[1] // 8:
        res.append("1")
    elif Window.size[1] // 8 <= pos[1] <= 2 * (Window.size[1] // 8):
        res.append("2")
    elif 2 * (Window.size[1] // 8) <= pos[1] <= 3 * (Window.size[1] // 8):
        res.append("3")
    elif 3 * (Window.size[1] // 8) <= pos[1] <= 4 * (Window.size[1] // 8):
        res.append("4")
    elif 4 * (Window.size[1] // 8) <= pos[1] <= 5 * (Window.size[1] // 8):
        res.append("5")
    elif 5 * (Window.size[1] // 8) <= pos[1] <= 6 * (Window.size[1] // 8):
        res.append("6")
    if 0 <= pos[0] <= Window.size[0] // 4:
        res.append("G")
    elif Window.size[0] // 4 <= pos[0] <= 2 * (Window.size[0] // 4):
        res.append("Y")
    elif 2 * (Window.size[0] // 4) <= pos[0] <= 3 * (Window.size[0] // 4):
        res.append("B")
    elif 3 * (Window.size[0] // 4) <= pos[0] <= Window.size[0]:
        res.append("R")
    return ''.join(res)


class FieldWidget(Widget):
    gamerposition = [[]]
    moveposition = ''

    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        with self.canvas:
            for y in range(0, 5 * Window.size[1] // 8, Window.size[1] // 8):
                Color(0, 1, 0)
                Ellipse(pos=(0, y), size_hint=(None, None), size=(Window.size[0] / 4, Window.size[1] // 8))
                Color(1, 1, 0)
                Ellipse(pos=(Window.size[0] // 4, y), size_hint=(None, None),
                        size=(Window.size[0] // 4, Window.size[1] // 8))
                Color(0, 0, 1)
                Ellipse(pos=(2 * Window.size[0] // 4, y), size_hint=(None, None),
                        size=(Window.size[0] // 4, Window.size[1] // 8))
                Color(1, 0, 0)
                Ellipse(pos=(3 * Window.size[0] // 4, y), size_hint=(None, None),
                        size=(Window.size[0] // 4, Window.size[1] // 8))

    def on_touch_down(self, touch):
        self.moveposition = define_circle(touch.pos)

    def on_touch_up(self, touch):
        removeposition = define_circle(touch.pos)
        if len(removeposition) == 2:
            for player in self.gamerposition:
                if removeposition in player:
                    player[player.index(removeposition)] = ''


class RouletteWidget(Widget):
    colorp = Color(1, 1, 1, 1)

    def __init__(self, **kwargs):
        super(RouletteWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.roulette = Ellipse(pos=(Window.size[0] - 100, Window.size[1] - 100), size=(200, 200))

    def change_color(self):
        c = self.canvas
        c.clear()
        with c:
            self.colorp = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            Color(rgba=self.colorp)
            self.roulette = Ellipse(pos=(Window.size[0] - 100, Window.size[1] - 100), size=(200, 200))


class MoveTimer(Label):
    a = NumericProperty(10)
    players = NumericProperty(3)

    def start(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a) + Animation(a=self.a, duration=0)

        def finish_callback(*args):
            roulette.change_color()
            i = int(player_move.text[-1])
            if len(field.moveposition) == 2:
                field.gamerposition[i - 1][field.gamerposition[i - 1].index('')] = field.moveposition
            if i == self.players:  # and player 1,2,3 or who did not lose
                player_move.text = "Player №1"
            else:
                player_move.text = "Player №" + str(i + 1)

        self.anim.repeat = True
        self.anim.bind(on_start=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = str(round(value, 1)) + " seconds"


field = FieldWidget(size_hint_y=0.875)
timer = MoveTimer()
roulette = RouletteWidget()
player_move = Label(text="Player №..")


class TwisterApp(App):

    def btn(*args):
        show_popup()

    def build(self):
        screen = BoxLayout(orientation="vertical")
        info = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        move = BoxLayout(orientation="vertical")
        move.add_widget(timer)
        move.add_widget(player_move)
        info.add_widget(move)
        settings = Button(background_normal="settings.png", background_down="settingsdown.png")
        settings.bind(on_press=self.btn)
        info.add_widget(settings)
        info.add_widget(roulette)
        screen.add_widget(info)
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
        roulette.change_color()
        player_move.text = "Player №0"
        field.gamerposition = [["" for x in range(fingers_slider.value)] for y in range(players_slider.value)]
        timer.start()

    popup.bind(on_dismiss=change_values)
    popup.open()


if __name__ == "__main__":
    TwisterApp().run()
