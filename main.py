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
step = Window.size[0] // 4


def define_circle(pos):
    res = []
    if 0 <= pos[1] <= step:
        res.append("1")
    elif step <= pos[1] <= 2 * step:
        res.append("2")
    elif 2 * step <= pos[1] <= 3 * step:
        res.append("3")
    elif 3 * step <= pos[1] <= 4 * step:
        res.append("4")
    elif 4 * step <= pos[1] <= 5 * step:
        res.append("5")
    elif 5 * step <= pos[1] <= 6 * step:
        res.append("6")
    if 0 <= pos[0] <= step:
        res.append("G")
    elif step <= pos[0] <= 2 * step:
        res.append("Y")
    elif 2 * step <= pos[0] <= 3 * step:
        res.append("B")
    elif 3 * step <= pos[0] <= Window.size[0]:
        res.append("R")
    return ''.join(res)


class FieldWidget(Widget):
    gamer_position = [[]]
    move_position = ''
    gamer_count = 0
    r_count = 0
    g_count = 0
    y_count = 0
    b_count = 0

    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        with self.canvas:
            for y in range(0, 6 * step, step):
                Color(0, 0, 0)
                Ellipse(pos=(0, y), size_hint=(None, None), size=(step, step))
                Color(1, 1, 1)
                Ellipse(pos=(1.5, y + 1.5), size_hint=(None, None), size=(step - 3, step - 3))
                Color(0, 1, 0)
                Ellipse(pos=(4, y + 4), size_hint=(None, None), size=(step - 8, step - 8))
                Color(0, 0, 0)
                Ellipse(pos=(step, y), size_hint=(None, None), size=(step, step))
                Color(1, 1, 1)
                Ellipse(pos=(step + 1.5, y + 1.5), size_hint=(None, None), size=(step - 3, step - 3))
                Color(1, 1, 0)
                Ellipse(pos=(step + 4, y + 4), size_hint=(None, None), size=(step - 8, step - 8))
                Color(0, 0, 0)
                Ellipse(pos=(2 * step, y), size_hint=(None, None), size=(step, step))
                Color(1, 1, 1)
                Ellipse(pos=(2 * step + 1.5, y + 1.5), size_hint=(None, None), size=(step - 3, step - 3))
                Color(0, 0, 1)
                Ellipse(pos=(2 * step + 4, y + 4), size_hint=(None, None), size=(step - 8, step - 8))
                Color(0, 0, 0)
                Ellipse(pos=(3 * step, y), size_hint=(None, None), size=(step, step))
                Color(1, 1, 1)
                Ellipse(pos=(3 * step + 1.5, y + 1.5), size_hint=(None, None), size=(step - 3, step - 3))
                Color(1, 0, 0)
                Ellipse(pos=(3 * step + 4, y + 4), size_hint=(None, None), size=(step - 8, step - 8))

    def update_field(self, position, upd):
        with self.canvas.after:
            if len(position) == 2:
                if position[1] == "R":
                    if upd:
                        Color(1, 0, 0)
                        Ellipse(pos=(3 * step, step * (int(position[0]) - 1)), size_hint=(None, None),
                                size=(step, step))
                    else:
                        Color(0, 0, 0)
                        Ellipse(pos=(3 * step, step * (int(position[0]) - 1)), size_hint=(None, None),
                                size=(step, step))
                        Color(1, 1, 1)
                        Ellipse(pos=(3 * step + 1.5, step * (int(position[0]) - 1) + 1.5), size_hint=(None, None),
                                size=(step - 3, step - 3))
                        Color(1, 0, 0)
                        Ellipse(pos=(3 * step + 4, step * (int(position[0]) - 1) + 4), size_hint=(None, None),
                                size=(step - 8, step - 8))
                if position[1] == "G":
                    if upd:
                        Color(0, 1, 0)
                        Ellipse(pos=(0, step * (int(position[0]) - 1)), size_hint=(None, None), size=(step, step))
                    else:
                        Color(0, 0, 0)
                        Ellipse(pos=(0, step * (int(position[0]) - 1)), size_hint=(None, None), size=(step, step))
                        Color(1, 1, 1)
                        Ellipse(pos=(1.5, step * (int(position[0]) - 1) + 1.5), size_hint=(None, None),
                                size=(step - 3, step - 3))
                        Color(0, 1, 0)
                        Ellipse(pos=(4, step * (int(position[0]) - 1) + 4), size_hint=(None, None),
                                size=(step - 8, step - 8))
                if position[1] == "B":
                    if upd:
                        Color(0, 0, 1)
                        Ellipse(pos=(2 * step, step * (int(position[0]) - 1)), size_hint=(None, None),
                                size=(step, step))
                    else:
                        Color(0, 0, 0)
                        Ellipse(pos=(2 * step, step * (int(position[0]) - 1)), size_hint=(None, None),
                                size=(step, step))
                        Color(1, 1, 1)
                        Ellipse(pos=(2 * step + 1.5, step * (int(position[0]) - 1) + 1.5), size_hint=(None, None),
                                size=(step - 3, step - 3))
                        Color(0, 0, 1)
                        Ellipse(pos=(2 * step + 4, step * (int(position[0]) - 1) + 4), size_hint=(None, None),
                                size=(step - 8, step - 8))
                if position[1] == "Y":
                    if upd:
                        Color(1, 1, 0)
                        Ellipse(pos=(step, step * (int(position[0]) - 1)), size_hint=(None, None),
                                size=(step, step))
                    else:
                        Color(0, 0, 0)
                        Ellipse(pos=(step, step * (int(position[0]) - 1)), size_hint=(None, None), size=(step, step))
                        Color(1, 1, 1)
                        Ellipse(pos=(step + 1.5, step * (int(position[0]) - 1) + 1.5), size_hint=(None, None),
                                size=(step - 3, step - 3))
                        Color(1, 1, 0)
                        Ellipse(pos=(step + 4, step * (int(position[0]) - 1) + 4), size_hint=(None, None),
                                size=(step - 8, step - 8))

    def on_touch_down(self, touch):
        self.move_position = define_circle(touch.pos)
        if player_move.text[-1] != "." and player_move.text[-1] != "!":
            i = int(player_move.text[-1])
            if self.gamer_position[i - 1] != "LOSER":
                if '' in self.gamer_position[i - 1]:
                    self.gamer_position[i - 1][self.gamer_position[i - 1].index('')] = self.move_position
                else:
                    self.gamer_position[i - 1][0] = "LOSER"
                    self.gamer_count -= 1
                if len(self.move_position) == 2:
                    if self.move_position[1] == "R":
                        self.r_count += 1
                    if self.move_position[1] == "G":
                        self.g_count += 1
                    if self.move_position[1] == "B":
                        self.b_count += 1
                    if self.move_position[1] == "Y":
                        self.y_count += 1
        self.update_field(self.move_position, True)

    def on_touch_up(self, touch):
        remove_position = define_circle(touch.pos)
        if player_move.text[-1] != "." and player_move.text[-1] != "!":
            if len(remove_position) == 2:
                for player in self.gamer_position:
                    if remove_position in player:
                        if "" in player and remove_position != self.move_position or (
                                self.gamer_position.index(player) + 1) != \
                                int(player_move.text[-1]):
                            player[0] = "LOSER"
                            self.gamer_count -= 1
                        else:
                            player[player.index(remove_position)] = ''
                if remove_position[1] == "R":
                    self.r_count -= 1
                if remove_position[1] == "G":
                    self.g_count -= 1
                if remove_position[1] == "B":
                    self.b_count -= 1
                if remove_position[1] == "Y":
                    self.y_count -= 1
        self.update_field(remove_position, False)


class RouletteWidget(Widget):
    roulette_color = Color(1, 1, 1, 1)

    def __init__(self, **kwargs):
        super(RouletteWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.roulette = Ellipse(pos=(Window.size[0] - step, Window.size[1] - step),
                                    size=(1.5 * step, 1.5 * step))

    def change_color(self):
        c = self.canvas
        c.clear()
        with c:
            self.roulette_color = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            while True:
                if self.roulette_color == (1, 0, 0, 1) and field.r_count != 6 or self.roulette_color == (
                        1, 1, 0, 1) and field.y_count != 6 or self.roulette_color == (
                        0, 1, 0, 1) and field.g_count != 6 or self.roulette_color == (
                        0, 0, 1, 1) and field.b_count != 6:
                    break
                else:
                    self.roulette_color = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            Color(rgba=self.roulette_color)
            self.roulette = Ellipse(pos=(Window.size[0] - step, Window.size[1] - step),
                                    size=(2 * step, 2 * step))


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
                if field.gamer_position[i - 1][0] != "LOSER":
                    break
            return i

        def finish_callback(*args):
            i = int(player_move.text[-1])
            if len(field.move_position) == 2 and (not (
                    field.move_position[1] == "B" and roulette.roulette_color == (0, 0, 1, 1) or field.move_position[
                1] == "R" and roulette.roulette_color == (1, 0, 0, 1) or field.move_position[
                        1] == "Y" and roulette.roulette_color == (
                            1, 1, 0, 1) or field.move_position[1] == "G" and roulette.roulette_color == (
                            0, 1, 0, 1)) or field.move_position not in field.gamer_position[i - 1]):
                field.gamer_position[i - 1][0] = "LOSER"
                field.gamer_count -= 1
            if len(field.move_position) < 2 and i != 0:
                field.gamer_position[i - 1][0] = "LOSER"
                field.gamer_count -= 1
            if field.gamer_count < 2:
                if field.gamer_count == 1:
                    for player in field.gamer_position:
                        if "LOSER" not in player:
                            player_move.text = f"Player №{field.gamer_position.index(player) + 1} win!"
                            timer.anim.stop(timer)
                if field.gamer_count < 1:
                    player_move.text = "No one win!"
                    timer.anim.stop(timer)
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
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        screen = BoxLayout(orientation="vertical")
        info = BoxLayout(orientation="horizontal", size_hint_y=0.12)
        move = BoxLayout(orientation="vertical")
        move.add_widget(timer)
        move.add_widget(player_move)
        info.add_widget(Widget(size_hint_x=0.125))
        info.add_widget(move)
        settings = Button(background_normal="settings.png", background_down="settingsdown.png", size_hint=(None, None),
                          size=(step - 15, step - 15))
        settings.bind(on_press=lambda x: show_settings())
        info.add_widget(settings)
        info.add_widget(roulette)
        screen.add_widget(info)
        screen.add_widget(field)
        return screen


def show_info():
    content = GridLayout(rows=2)
    about = Label(
        text="This is a Twister game for Android.\nThe rules of the game are similar to the rules of the original "
             "[i]Twister[/i]. On the playing field there are special sections (4 rows of 6 circles) of different "
             "colors, "
             "on one of which the player puts his finger for a limited time at the direction of the roulette and "
             "holds it until the end of the game or a change of position as a result of the next scrolling of the "
             "roulette.\nThe game is played by 2 to 10 players, each of whom can put on the field from 1 to 5 fingers "
             "of one hand, the turn time is set from 5 to 15 seconds (these game settings are located in a separate "
             "menu). The winner is the last player remaining in the field.\n[b]A player is eliminated from the game if "
             "he[/b]: "
             "does not put his finger in the specified place during his turn, removes his finger not in his turn, "
             "regardless of the move removes his finger, provided that not all fingers are on the field.",
        size_hint=(1, 0.9), text_size=(Window.size[0] - 15, None), markup=True, font_size="13sp")
    ok = Button(text="Ok", size_hint=(1, 0.1))
    content.add_widget(about)
    content.add_widget(ok)
    popup = Popup(title="Game info", content=content, auto_dismiss=False)
    ok.bind(on_press=popup.dismiss)
    popup.open()


def show_settings():
    content = GridLayout(cols=3)
    content.add_widget(Label(text="Players"))
    players_label = Label(text="6")
    players_slider = Slider(min=2, max=10, value=6, step=1, cursor_size=(75, 75))
    content.add_widget(players_label)
    content.add_widget(players_slider)
    content.add_widget(Label(text="Fingers"))
    fingers_label = Label(text="3")
    fingers_slider = Slider(min=1, max=5, value=3, step=1, cursor_size=(75, 75))
    content.add_widget(fingers_label)
    content.add_widget(fingers_slider)
    content.add_widget(Label(text="Time for move"))
    time_label = Label(text="10")
    time_slider = Slider(min=5, max=15, value=10, step=5, cursor_size=(75, 75))
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
    popup = Popup(title="Game settings", content=content, auto_dismiss=False)
    ok.bind(on_press=popup.dismiss)

    def change_values(*args):
        timer.a = time_slider.value
        timer.players = players_slider.value
        roulette.change_color()
        field.gamer_position = [["" for x in range(fingers_slider.value)] for y in range(players_slider.value)]
        player_move.text = "Player №0"
        field.gamer_count = players_slider.value
        field.r_count = 0
        field.g_count = 0
        field.y_count = 0
        field.b_count = 0
        timer.start()

    popup.bind(on_dismiss=change_values)
    popup.open()


if __name__ == "__main__":
    TwisterApp().run()
