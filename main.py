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
# Определение размера для размещения секций игрового поля
step = Window.size[0] // 4


# Метод для определения секции (ряд и цвет), с которой произошло взаимодействие
def define_circle(pos):
    res = []
    # Определение ряда
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
    # Определение цвета
    if 0 <= pos[0] <= step:
        res.append("G")
    elif step <= pos[0] <= 2 * step:
        res.append("Y")
    elif 2 * step <= pos[0] <= 3 * step:
        res.append("B")
    elif 3 * step <= pos[0] <= Window.size[0]:
        res.append("R")
    return ''.join(res)


# Класс, отвечающей за отрисовку игрового поля и подсчет параметров игры (число оставшихся игроков, позиция хода,
# позиции, занятые игроками, количество свободных секций каждого отдельного цвета, которое понадобится для рулетки)
class FieldWidget(Widget):
    # Позиции игроков на поле
    gamer_position = [[]]
    # Позиция данного хода игрока
    move_position = ''
    # Счетчик невыбывших игроков
    gamer_count = 0
    # Счетчики занятых полей отдельных цветов, необходимые для определения следующего хода
    r_count = 0
    g_count = 0
    y_count = 0
    b_count = 0

    # Начальная отрисовка игрового поля
    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        with self.canvas:
            for y in range(0, 6 * step, step):
                # Зеленый круг
                Color(0, 0.5, 0)
                Ellipse(pos=(0.5, y + 0.5), size_hint=(None, None), size=(step - 5, step - 5))
                Color(0, 1, 0)
                Ellipse(pos=(4, y + 8), size_hint=(None, None), size=(step - 10, step - 10))
                # Желтый круг
                Color(0.5, 0.5, 0)
                Ellipse(pos=(step + 0.5, y + 0.5), size_hint=(None, None), size=(step - 5, step - 5))
                Color(1, 1, 0)
                Ellipse(pos=(step + 4, y + 8), size_hint=(None, None), size=(step - 10, step - 10))
                # Синий круг
                Color(0, 0, 0.5)
                Ellipse(pos=(2 * step + 0.5, y + 0.5), size_hint=(None, None), size=(step - 5, step - 5))
                Color(0, 0, 1)
                Ellipse(pos=(2 * step + 4, y + 8), size_hint=(None, None), size=(step - 10, step - 10))
                # Красный круг
                Color(0.5, 0, 0)
                Ellipse(pos=(3 * step + 0.5, y + 0.5), size_hint=(None, None), size=(step - 5, step - 5))
                Color(1, 0, 0)
                Ellipse(pos=(3 * step + 4, y + 8), size_hint=(None, None), size=(step - 10, step - 10))

    # Обновление поля в результате нажатия, отрисовка зажатых секций
    def update_field(self, position, upd):
        with self.canvas.after:
            if len(position) == 2:
                if position[1] == "R":
                    if upd:
                        Color(1, 1, 1)
                        Ellipse(pos=(3 * step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                        Color(1, 0, 0)
                        Ellipse(pos=(3 * step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                    else:
                        Color(0.5, 0, 0)
                        Ellipse(pos=(3 * step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                        Color(1, 0, 0)
                        Ellipse(pos=(3 * step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                if position[1] == "G":
                    if upd:
                        Color(1, 1, 1)
                        Ellipse(pos=(4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                        Color(0, 1, 0)
                        Ellipse(pos=(0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                    else:
                        Color(0, 0.5, 0)
                        Ellipse(pos=(0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                        Color(0, 1, 0)
                        Ellipse(pos=(4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                if position[1] == "B":
                    if upd:
                        Color(1, 1, 1)
                        Ellipse(pos=(2 * step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                        Color(0, 0, 1)
                        Ellipse(pos=(2 * step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                    else:
                        Color(0, 0, 0.5)
                        Ellipse(pos=(2 * step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                        Color(0, 0, 1)
                        Ellipse(pos=(2 * step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                if position[1] == "Y":
                    if upd:
                        Color(1, 1, 1)
                        Ellipse(pos=(step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))
                        Color(1, 1, 0)
                        Ellipse(pos=(step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                    else:
                        Color(0.5, 0.5, 0)
                        Ellipse(pos=(step + 0.5, step * (int(position[0]) - 1) + 0.5), size_hint=(None, None),
                                size=(step - 5, step - 5))
                        Color(1, 1, 0)
                        Ellipse(pos=(step + 4, step * (int(position[0]) - 1) + 8), size_hint=(None, None),
                                size=(step - 10, step - 10))

    # Обработка нажатия на экран (определение положения, игрока и возможного выбывания игрока по причинам, описываемым
    # в правилах)
    def on_touch_down(self, touch):
        # Определение положения нажатия
        self.move_position = define_circle(touch.pos)
        # Определение, идет ли в данный момент игра
        if player_move.text[-1] != "." and player_move.text[-1] != "!":
            # Определение номера игрока, который ходит в данный момент
            i = int(player_move.text[-1])
            # Если игрок не выбыл из игры
            if self.gamer_position[i - 1] != "LOSER":
                # Если игрок разместил не все пальцы на игровом поле, его ход записывается в соответствующую ячейку
                # массива
                if '' in self.gamer_position[i - 1]:
                    self.gamer_position[i - 1][self.gamer_position[i - 1].index('')] = self.move_position
                else:
                    self.gamer_position[i - 1][0] = "LOSER"
                    self.gamer_count -= 1
                # Определение цвета занятой в результате нажатия ячейки игрового поля
                if len(self.move_position) == 2:
                    if self.move_position[1] == "R":
                        self.r_count += 1
                    if self.move_position[1] == "G":
                        self.g_count += 1
                    if self.move_position[1] == "B":
                        self.b_count += 1
                    if self.move_position[1] == "Y":
                        self.y_count += 1
        # Обновление игрового поля после нажатия
        self.update_field(self.move_position, True)

    # Обработка отпускания пальца (определение положения, игрока и возможного выбывания игрока по причинам,
    # описываемым в правилах игры)
    def on_touch_up(self, touch):
        # Определение положения отпускания
        remove_position = define_circle(touch.pos)
        # Определение, идет ли в данный момент игра
        if player_move.text[-1] != "." and player_move.text[-1] != "!":
            if len(remove_position) == 2:
                for player in self.gamer_position:
                    # Определение игрока, отпустившего палец по положению отпускания
                    if remove_position in player:
                        # Если игрок на момент отпускания разместил не все пальцы на поле и при этом позиция
                        # отпускания не соответствует позиции нажатия или же в данный момент ходит не этот игрок,
                        # то игрок выбывает из игры
                        if "" in player and remove_position != self.move_position or (
                                self.gamer_position.index(player) + 1) != \
                                int(player_move.text[-1]):
                            player[0] = "LOSER"
                            self.gamer_count -= 1
                        # В противном случае удаляем из массива ходов игрока запись о ходе в данной позиции
                        else:
                            player[player.index(remove_position)] = ''
                # Определение цвета освобожденной в результате отпускания ячейки игрового поля
                if remove_position[1] == "R":
                    self.r_count -= 1
                if remove_position[1] == "G":
                    self.g_count -= 1
                if remove_position[1] == "B":
                    self.b_count -= 1
                if remove_position[1] == "Y":
                    self.y_count -= 1
        # Обновление игрового поля после отпускания
        self.update_field(remove_position, False)


# Класс, отображающий рулетку на игровом поле
class RouletteWidget(Widget):
    # Цвет рулетки
    roulette_color = Color(1, 1, 1, 1)

    def __init__(self, **kwargs):
        super(RouletteWidget, self).__init__(**kwargs)
        with self.canvas:
            # Перед началом игры цвет рулетки белый
            Color(1, 1, 1, 1)
            # Рулетка представляет собой окружность, расположенную в правом верхнем углу экрана
            self.roulette = Ellipse(
                pos=(Window.size[0] - 0.75 * step, Window.size[1] - 0.75 * step),
                size=(1.5 * step, 1.5 * step))

    # Метод, отвечающий за смену цветов рулетки
    def change_color(self):
        c = self.canvas
        c.clear()
        with c:
            self.roulette_color = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            while True:
                # Определяем, есть ли у игрока возможность поставить палец на секцию указанного цвета (свободна ли
                # ячейка указанного цвета)
                if self.roulette_color == (1, 0, 0, 1) and field.r_count != 6 or self.roulette_color == (
                        1, 1, 0, 1) and field.y_count != 6 or self.roulette_color == (
                        0, 1, 0, 1) and field.g_count != 6 or self.roulette_color == (
                        0, 0, 1, 1) and field.b_count != 6:
                    break
                # Если все ячейки указанного цвета заняты, то выбираем другой цвет
                else:
                    self.roulette_color = random.choice([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)])
            Color(rgba=self.roulette_color)
            # Перерисовываем окружность на той же позиции, но другого цвета
            self.roulette = Ellipse(
                pos=(Window.size[0] - 0.75 * step, Window.size[1] - 0.75 * step),
                size=(1.5 * step, 1.5 * step))


# Класс, описывающий таймер хода на игровом поле
class MoveTimer(Label):
    # Длительность хода, задаваемая в настройках игры (изначально используется значение по умолчанию)
    a = NumericProperty(10)
    # Число игроков (изначально используется значение по умолчанию)
    players = NumericProperty(3)

    # Метод, описывающей начало анимации таймера
    def start(self):
        Animation.cancel_all(self)
        # Анимация таймера состоит из двух последовательных частей (отсчет времени, равного длительности хода,
        # и возвращение к значению, равному длительности следующего хода)
        self.anim = Animation(a=0, duration=self.a) + Animation(a=self.a, duration=0)

        # Метод, отвечающий за поиск следующего невыбывшего игрока
        def find_next(i):
            while True:
                i += 1
                if i > self.players:
                    i = 1
                # Если игрок не выбыл, то он будет ходить следующим
                if field.gamer_position[i - 1][0] != "LOSER":
                    break
            return i

        # Метод, отвечающий за действия после окончания хода (определение выбывания игрока, смена цвета рулетки,
        # поиск следующего игрока)
        def finish_callback(*args):
            # Определение номера игрока, сыгравшего данный ход
            i = int(player_move.text[-1])
            # Если игрок нажал на окружность цвета, отличного от указанного на рулетке, то он выбывает из игры
            if len(field.move_position) == 2 and (not (
                    field.move_position[1] == "B" and roulette.roulette_color == (0, 0, 1, 1) or field.move_position[
                1] == "R" and roulette.roulette_color == (1, 0, 0, 1) or field.move_position[
                        1] == "Y" and roulette.roulette_color == (
                            1, 1, 0, 1) or field.move_position[1] == "G" and roulette.roulette_color == (
                            0, 1, 0, 1)) or field.move_position not in field.gamer_position[i - 1]):
                field.gamer_position[i - 1][0] = "LOSER"
                field.gamer_count -= 1
            # Если в данный момент идет игра и игрок не нажал на игровое поле во время своего хода, то он выбывает
            if len(field.move_position) < 2 and i != 0:
                field.gamer_position[i - 1][0] = "LOSER"
                field.gamer_count -= 1
            # Если осталось меньше двух невыбывших игроков
            if field.gamer_count < 2:
                # Если остался один невыбывших игрок, определяется его номер, отображается сообщение о том,
                # что этот игрок победил, и игра останавливается
                if field.gamer_count == 1:
                    for player in field.gamer_position:
                        # Если данный игрок не выбыл из игры
                        if "LOSER" not in player:
                            # Вывод сообщения о победе игрока в текстовом поле, содержащем информацию о состоянии
                            # игры, зеленым цветом и остановка таймера игры
                            player_move.text = f"Player №{field.gamer_position.index(player) + 1} won!"
                            player_move.color = (0, 1, 0, 1)
                            timer.anim.stop(timer)
                # Если на поле не осталось невыбывших игроков, отображается сообщение о том, что победителей нет, и игра
                # останавливается
                if field.gamer_count < 1:
                    # Вывод сообщения о поражении всех игроков в текстовом поле, содержащем информацию о состоянии
                    # игры, красным цветом и остановка таймера игры
                    player_move.text = "No one won!"
                    player_move.color = (1, 0, 0, 1)
                    timer.anim.stop(timer)
            # Если невыбывших игроков больше одного, то цвет рулетки изменяется и отображается сообщение с номером
            # игрока, который ходит следующим (при этом счетчик заново отсчитывает время хода игрока)
            else:
                roulette.change_color()
                player_move.text = f"Player №{find_next(i)}"

        # Задание повторения последовательной анимации
        self.anim.repeat = True
        self.anim.bind(on_start=finish_callback)
        self.anim.start(self)

    # Метод, отвечающий за отображение таймера на игровом поле
    def on_a(self, instance, value):
        self.text = f"{round(value, 1)} seconds"


# Создание игрового поля
field = FieldWidget(size_hint_y=0.875)
# Создание таймера
timer = MoveTimer(color=(0, 0, 0, 1))
# Создание рулетки
roulette = RouletteWidget()
# Добавление текстового поля с сообщениями о состоянии игры
player_move = Label(text="Player №..", color=(0, 0, 0, 1))


# Класс, отвечающий за отрисовку главного экрана приложения
class TwisterApp(App):
    def build(self):
        # Фон приложения - белый
        Window.clearcolor = (1, 1, 1, 1)
        # Размещение виджетов по вертикали
        screen = BoxLayout(orientation="vertical")
        # Отступ для лучшего отображения информационных виджетов
        screen.add_widget(Widget(size_hint_y=0.03))
        # Создание горизонтальной панели информационных виджетов
        info = BoxLayout(orientation="horizontal", size_hint_y=0.1)
        # Левая часть информационной панели состоит из 2 вертикально расположенных виджетов: таймера хода и
        # текстового поля с сообщениями о состоянии игры
        move = BoxLayout(orientation="vertical")
        # Таймер хода
        move.add_widget(timer)
        # Текстовое поле с сообщениями о состоянии игры
        move.add_widget(player_move)
        # Отступ для лучшего отображения текстового поля
        info.add_widget(Widget(size_hint_x=0.1))
        # Добавление панели информационных виджетов к горизонтальной панели в верхней части экрана
        info.add_widget(move)
        # Создание кнопки включения настроек, среди параметров которой изображение кнопки в двух состояниях (обычном
        # и нажатом), размеры кнопки и метод, вызываемый при нажатии
        settings = Button(background_normal="settings.png", background_down="settingsdown.png", size_hint=(None, None),
                          size=(step - 30, step - 30), on_press=lambda x: show_settings())
        # Добавление кнопки к горизонтальной панели в верхней части экрана
        info.add_widget(settings)
        # Добавление рулетки к горизонтальной панели в верхней части экрана
        info.add_widget(roulette)
        # Добавление панели информационных виджетов в верхнюю часть экрана приложения
        screen.add_widget(info)
        # Добавление игрового поля к главному экрану приложения
        screen.add_widget(field)
        # Отображение главного экрана приложения
        return screen


# Метод, отвечающий за отображение всплывающего окна информации об игре
def show_info():
    # Содержимое всплывающего окна расположено в таблице из двух вертикально расположенных ячеек
    content = GridLayout(rows=2)
    # Создание текстового поля с информацией об игре, среди параметров которого размеры виджета, размеры текста,
    # использование разметки и размер шрифта
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
        size_hint=(0.9, 0.9), text_size=(Window.size[0] - 15, None), markup=True, font_size="13sp")
    # Создание кнопки, отвечающая за закрытие всплывающего окна
    ok = Button(text="Ok", size_hint=(1, 0.1))
    # Добавление текстового поля
    content.add_widget(about)
    # Добавление кнопки
    content.add_widget(ok)
    # Создание всплывающего окна, среди параметров которого название окна и содержимое, созданное выше
    popup = Popup(title="Game info", content=content, auto_dismiss=False)
    # Добавление к кнопке опции закрытия всплывающего окна
    ok.bind(on_press=popup.dismiss)
    # Открытие всплывающего окна
    popup.open()


# Метод, отвечающий за отображение всплывающего окна настроек игры
def show_settings():
    # Содержимое всплывающего окна расположено в таблице, содержащей три колонки
    content = GridLayout(cols=3)
    # Добавление регулируемых настроек игрового процесса: количества игроков, количества пальцев у каждого игрока и
    # количество времени на каждый ход
    content.add_widget(Label(text="Players"))
    # Значение количества игроков по умолчанию
    players_label = Label(text="6")
    # Создание ползунка для настройки количества игроков с возможностью регулировки от 2 до 10
    players_slider = Slider(min=2, max=10, value=6, step=1, cursor_size=(75, 75))
    content.add_widget(players_label)
    content.add_widget(players_slider)
    content.add_widget(Label(text="Fingers"))
    # Значение количества пальцев по умолчанию
    fingers_label = Label(text="3")
    # Создание ползунка для настройки количества пальцев с возможностью регулировки от 1 до 5
    fingers_slider = Slider(min=1, max=5, value=3, step=1, cursor_size=(75, 75))
    content.add_widget(fingers_label)
    content.add_widget(fingers_slider)
    content.add_widget(Label(text="Time for move"))
    # Значение времени на один ход по умолчанию
    time_label = Label(text="10")
    # Создание ползунка для настройки времени на один ход с возможностью переключения между 5, 10 и 15 секундами
    time_slider = Slider(min=5, max=15, value=10, step=5, cursor_size=(75, 75))
    content.add_widget(time_label)
    content.add_widget(time_slider)

    # Методы, отвечающие за отображение значения ползунка в текстовом поле слева от ползунка
    def on_p_slider_value_change(instance, value):
        players_label.text = str(value)

    def on_f_slider_value_change(instance, value):
        fingers_label.text = str(value)

    def on_t_slider_value_change(instance, value):
        time_label.text = str(value)

    players_slider.bind(value=on_p_slider_value_change)
    fingers_slider.bind(value=on_f_slider_value_change)
    time_slider.bind(value=on_t_slider_value_change)

    # Добавление кнопки, отвечающей за открытие всплывающего окна с информацией об игре
    content.add_widget(Button(text="About", on_press=lambda x: show_info()))
    content.add_widget(Widget())
    # Создание кнопки, отвечающей за закрытие всплывающего окна настройки игры
    ok = Button(text="Ok")
    content.add_widget(ok)
    # Создание всплывающего окна, среди параметров которого название окна и содержимое, созданное выше
    popup = Popup(title="Game settings", content=content, auto_dismiss=False)
    # Добавление к кнопке опции закрытия всплывающего окна
    ok.bind(on_press=popup.dismiss)

    # Изменение значений параметров после их задания во всплывающем меню настроек
    def change_values(*args):
        # Задание нового значения для таймера хода
        timer.a = time_slider.value
        # Задание нового значения количества игроков
        timer.players = players_slider.value
        # Изменение цвета рулетки
        roulette.change_color()
        # Инициализация массива ходов игроков размерности (количество игроков x количество пальцев)
        field.gamer_position = [["" for x in range(fingers_slider.value)] for y in range(players_slider.value)]
        # Изменение текстового поля с сообщением о состоянии игры, которое изменится сразу после начала игры
        player_move.text = "Player №0"
        # Изменение цвета текстового поля
        player_move.color = (0, 0, 0, 1)
        # Задание значения количества невыбывших игроков
        field.gamer_count = players_slider.value
        # Задание значения свободных ячеек различных цветов на момент начала игры
        field.r_count = 0
        field.g_count = 0
        field.y_count = 0
        field.b_count = 0
        # Начало игры
        timer.start()

    # Добавление к всплывающему окну метода, приведенного выше, который будет вызываться при закрытии всплывающего окна
    popup.bind(on_dismiss=change_values)
    # Открытие всплывающего окна
    popup.open()


# Запуск приложения
if __name__ == "__main__":
    TwisterApp().run()
