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
field_step = Window.size[0] // 4


def define_circle(pos):
    res = []
    if 0 <= pos[1] <= field_step:
        res.append("1")
    elif field_step <= pos[1] <= 2 * field_step:
        res.append("2")
    elif 2 * field_step <= pos[1] <= 3 * field_step:
        res.append("3")
    elif 3 * field_step <= pos[1] <= 4 * field_step:
        res.append("4")
    elif 4 * field_step <= pos[1] <= 5 * field_step:
        res.append("5")
    elif 5 * field_step <= pos[1] <= 6 * field_step:
        res.append("6")
    if 0 <= pos[0] <= field_step:
        res.append("G")
    elif field_step <= pos[0] <= 2 * field_step:
        res.append("Y")
    elif 2 * field_step <= pos[0] <= 3 * field_step:
        res.append("B")
    elif 3 * field_step <= pos[0] <= Window.size[0]:
        res.append("R")
    return ''.join(res)


class FieldWidget(Widget):
    gamerposition = [[]]
    moveposition = ''
    gamercount = 0
    Rcount = 0
    Gcount = 0
    Ycount = 0
    Bcount = 0

    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        with self.canvas:
            for y in range(0, 5 * field_step, field_step):
                Color(0, 1, 0)
                Ellipse(pos=(0, y), size_hint=(None, None), size=(Window.size[0] / 4, field_step))
                Color(1, 1, 0)
                Ellipse(pos=(field_step, y), size_hint=(None, None),
                        size=(field_step, field_step))
                Color(0, 0, 1)
                Ellipse(pos=(2 * field_step, y), size_hint=(None, None),
                        size=(field_step, field_step))
                Color(1, 0, 0)
                Ellipse(pos=(3 * field_step, y), size_hint=(None, None),
                        size=(field_step, field_step))

    def on_touch_down(self, touch):
        self.moveposition = define_circle(touch.pos)
        if player_move.text[-1] != "." and player_move.text[-1] != "!":
            i = int(player_move.text[-1])
            if self.gamerposition[i - 1] != "LOSER":
                self.gamerposition[i - 1][self.gamerposition[i - 1].index('')] = self.moveposition
                if len(self.moveposition) == 2:
                    if self.moveposition[1] == "R":
                        self.Rcount += 1
                    if self.moveposition[1] == "G":
                        self.Gcount += 1
                    if self.moveposition[1] == "B":
                        self.Bcount += 1
                    if self.moveposition[1] == "Y":
                        self.Ycount += 1

    def on_touch_up(self, touch):
        removeposition = define_circle(touch.pos)
        if len(removeposition) == 2:
            for player in self.gamerposition:
                if removeposition in player:
                    if "" in player and removeposition != self.moveposition or (self.gamerposition.index(player) + 1) != \
                            player_move.text[-1]:
                        player[0] = "LOSER"
                        self.gamercount -= 1
                    player[player.index(removeposition)] = ''
            if removeposition[1] == "R":
                self.Rcount -= 1
            if removeposition[1] == "G":
                self.Gcount -= 1
            if removeposition[1] == "B":
                self.Bcount -= 1
            if removeposition[1] == "Y":
                self.Ycount -= 1

    def find_winner(self):
        for player in self.gamerposition:
            if "LOSER" not in player:
                return self.gamerposition.index(player) + 1
        return -1


class RouletteWidget(Widget):
    colorp = Color(1, 1, 1, 1)

    def __init__(self, **kwargs):
        super(RouletteWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.roulette = Ellipse(pos=(Window.size[0] - field_step, Window.size[1] - field_step),
                                    size=(2 * field_step, 2 * field_step))

    def change_color(self):
        c = self.canvas
        c.clear()
        with c:
            self.colorp = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            while True:
                if self.colorp == (1, 0, 0, 1) and field.Rcount != 6 or self.colorp == (
                        1, 1, 0, 1) and field.Ycount != 6 or self.colorp == (
                        0, 1, 0, 1) and field.Gcount != 6 or self.colorp == (0, 0, 1, 1) and field.Bcount != 6:
                    break
                else:
                    self.colorp = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            Color(rgba=self.colorp)
            self.roulette = Ellipse(pos=(Window.size[0] - field_step, Window.size[1] - field_step),
                                    size=(2 * field_step, 2 * field_step))


class MoveTimer(Label):
    a = NumericProperty(10)
    players = NumericProperty(3)

    def start(self):
        Animation.cancel_all(self)
        self.anim = Animation(a=0, duration=self.a) + Animation(a=self.a, duration=0)

        def find_next(i):
            while True:
                i += 1
                if i > self.players:
                    i = 1
                if field.gamerposition[i - 1][0] != "LOSER":
                    break
            return i

        def finish_callback(*args):
            i = int(player_move.text[-1])
            if len(field.moveposition) == 2 and (not (
                    field.moveposition[1] == "B" and roulette.colorp == (0, 0, 1, 1) or field.moveposition[
                1] == "R" and roulette.colorp == (1, 0, 0, 1) or field.moveposition[1] == "Y" and roulette.colorp == (
                            1, 1, 0, 1) or field.moveposition[1] == "G" and roulette.colorp == (
                            0, 1, 0, 1)) or field.moveposition not in field.gamerposition[i - 1]):
                field.gamerposition[i - 1][0] = "LOSER"
                field.gamercount -= 1
            if len(field.moveposition) < 2 and i != 0:
                field.gamerposition[i - 1][0] = "LOSER"
                field.gamercount -= 1
            if field.gamercount == 1:
                player_move.text = f"Player №{field.find_winner()} win!"
                self.anim.stop(self)
            else:
                roulette.change_color()
                player_move.text = f"Player №{find_next(i)}"

        self.anim.repeat = True
        self.anim.bind(on_start=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        self.text = f"{round(value, 1)} seconds"


field = FieldWidget(size_hint_y=0.875)
timer = MoveTimer(color=(0, 0, 0, 1))
roulette = RouletteWidget()
player_move = Label(text="Player №..", color=(0, 0, 0, 1))


class TwisterApp(App):

    def btn(*args):
        show_settings()

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        screen = BoxLayout(orientation="vertical")
        info = BoxLayout(orientation="horizontal", size_hint_y=0.15)
        move = BoxLayout(orientation="vertical")
        move.add_widget(timer)
        move.add_widget(player_move)
        info.add_widget(move)
        settings = Button(background_normal="settings.png", background_down="settingsdown.png")
        settings.bind(on_press=lambda x: show_settings())
        info.add_widget(settings)
        info.add_widget(roulette)
        screen.add_widget(info)
        screen.add_widget(field)
        return screen


def show_info():
    content = BoxLayout(orientation="vertical")
    about = Label(text="Это Твистер.")
    ok = Button(text="Ok")
    content.add_widget(about)
    content.add_widget(ok)
    popup = Popup(title='Game info', content=content, auto_dismiss=False)
    ok.bind(on_press=popup.dismiss)
    popup.open()


def show_settings():
    content = GridLayout(cols=3)
    content.add_widget(Label(text="Players"))
    players_label = Label(text="3")
    players_slider = Slider(min=2, max=5, value=3, step=1)
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

    def on_p_slider_value_change(instance, value):
        players_label.text = str(value)

    def on_f_slider_value_change(instance, value):
        fingers_label.text = str(value)

    def on_t_slider_value_change(instance, value):
        time_label.text = str(value)

    players_slider.bind(value=on_p_slider_value_change)
    fingers_slider.bind(value=on_f_slider_value_change)
    time_slider.bind(value=on_t_slider_value_change)

    content.add_widget(Button(text="About", on_press=lambda x: show_info()))
    content.add_widget(Widget())
    ok = Button(text="Ok")
    content.add_widget(ok)
    popup = Popup(title='Game settings', content=content, auto_dismiss=False)
    ok.bind(on_press=popup.dismiss)

    def change_values(instance):
        timer.a = time_slider.value
        timer.players = players_slider.value
        roulette.change_color()
        field.gamerposition = [["" for x in range(fingers_slider.value)] for y in range(players_slider.value)]
        player_move.text = "Player №0"
        field.gamercount = players_slider.value
        timer.start()

    popup.bind(on_dismiss=change_values)
    popup.open()


if __name__ == "__main__":
    TwisterApp().run()
