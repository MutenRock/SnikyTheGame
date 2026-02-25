from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
import random

class Player(Image):
    line_index = NumericProperty(0)
    ammo = NumericProperty(0)
    flicker_timer = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.source = 'sprites/player/sniky.png'
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos = (50, self.parent.line_positions[self.line_index] if self.parent else 0)

    def move_up(self):
        if self.parent:
            self.line_index = (self.line_index - 1) % len(self.parent.line_positions)
            self.pos = (self.pos[0], self.parent.line_positions[self.line_index])

    def move_down(self):
        if self.parent:
            self.line_index = (self.line_index + 1) % len(self.parent.line_positions)
            self.pos = (self.pos[0], self.parent.line_positions[self.line_index])

    def draw_ammo(self):
        if self.ammo > 0:
            ammo_label = Label(text=str(self.ammo), pos=(self.x, self.y + self.height), font_size='20sp')
            self.parent.add_widget(ammo_label)
            Clock.schedule_once(lambda dt: self.parent.remove_widget(ammo_label), 0.5)

class Enemy(Image):
    speed_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.source = random.choice([
            'sprites/enemies/enemy1.png',
            'sprites/enemies/enemy2.png',
            'sprites/enemies/enemy3.png',
            'sprites/enemies/enemy4.png'
        ])
        self.size_hint = (None, None)
        self.size = (self.width / 5, self.height / 5)
        self.pos = (self.parent.width, random.choice(self.parent.line_positions))
        self.speed_x = random.randint(2, 4)

    def update(self, dt):
        self.x -= self.speed_x
        if self.x < 0:
            self.parent.remove_widget(self)
        if self.collide_widget(self.parent.player):
            self.parent.game_over()

class Bonus(Image):
    def __init__(self, **kwargs):
        super(Bonus, self).__init__(**kwargs)
        self.source = 'sprites/items/weapon.png'
        self.size_hint = (None, None)
        self.size = (self.width / 6, self.height / 6)
        self.pos = (self.parent.width, random.choice(self.parent.line_positions))
        self.speed_x = 2

    def update(self, dt):
        self.x -= self.speed_x
        if self.collide_widget(self.parent.player):
            self.parent.player.ammo += 3
            if self.parent.player.ammo > 10:
                self.parent.player.ammo = 10
            self.parent.remove_widget(self)
            self.parent.player.flicker_timer = 12

class GameWidget(FloatLayout):
    player = ObjectProperty(None)
    line_positions = []

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        with self.canvas:
            self.bg = Rectangle(source='backgrounds/background_game.png', pos=self.pos, size=self.size)
            self.bind(pos=self.update_bg, size=self.update_bg)

        self.line_positions = [self.height // 5 * i for i in range(1, 5)]
        self.player = Player()
        self.add_widget(self.player)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 1.0)
        Clock.schedule_interval(self.spawn_bonus, 5.0)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def update(self, dt):
        for child in self.children:
            if isinstance(child, Enemy) or isinstance(child, Bonus):
                child.update(dt)

    def spawn_enemy(self, dt):
        enemy = Enemy()
        self.add_widget(enemy)

    def spawn_bonus(self, dt):
        bonus = Bonus()
        self.add_widget(bonus)

    def game_over(self):
        self.clear_widgets()
        game_over_label = Label(text='Game Over', font_size='50sp', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(game_over_label)
        Clock.schedule_once(lambda dt: self.parent.switch_to_menu(), 2)

class SnikyApp(App):
    def build(self):
        game = GameWidget()
        return game

if __name__ == '__main__':
    SnikyApp().run()
