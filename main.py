from kivy.app import App
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

    def start_game(self, *args):
        self.serve_ball()
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def quit_game(self, *args):
        App.get_running_app().stop()

class MainMenu(FloatLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        self.label = Label(text='PONG GAME', font_size=50, size_hint=(1, 0.2), pos_hint={'top': 1})
        self.add_widget(self.label)

        self.play_button = Button(text='PLAY', font_size=30, size_hint=(0.5, 0.2), pos_hint={'x': 0.25, 'y': 0.4})
        self.play_button.bind(on_release=self.start_pong)
        self.add_widget(self.play_button)

        self.quit_button = Button(text='QUIT', font_size=30, size_hint=(0.5, 0.2), pos_hint={'x': 0.25, 'y': 0.2})
        self.quit_button.bind(on_release=self.quit_game)
        self.add_widget(self.quit_button)

    def start_pong(self, *args):
        game = PongGame()
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(game)
        game.start_game()

    def quit_game(self, *args):
        App.get_running_app().stop()

class PongApp(App):
    def build(self):
        menu = MainMenu()
        return menu

if __name__ == '__main__':
    PongApp().run()