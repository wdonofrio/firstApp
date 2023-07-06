from src.logging_config import logger
from src.decorators import log_method

import csv
from random import randint

from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from kivy.core.audio import SoundLoader

POP_SOUND = SoundLoader.load("audio/POP.WAV")


class ConcreteObject:
    @log_method
    def bounce_ball(self, ball, velocity=1.0):
        if self.collide_widget(ball):
            offset_x = (ball.center_x - self.center_x) / (self.width / 2)
            offset_y = (ball.center_y - self.center_y) / (self.height / 2)
            logger.info(f"{offset_x}, {offset_y}")
            # Adjust the offset based on which corner the ball collides with
            if offset_x > 0:
                offset_x = 1 - offset_x
            else:
                offset_x = -1 - offset_x

            if offset_y > 0:
                offset_y = 1 - offset_y
            else:
                offset_y = -1 - offset_y

            ball.velocity = (
                ball.velocity[0] * velocity + offset_x,
                ball.velocity[1] * velocity + offset_y,
            )
            POP_SOUND.play()


class Brick(Widget, ConcreteObject):
    def __init__(self, **kwargs):
        super(Brick, self).__init__(**kwargs)
        self.width, self.height = 30, 30
        self.size = (self.width, self.height)
        self.position = 0, 0

    @log_method
    def set_position(self, row_index, col_index):
        brick_width, brick_height = self.size
        spacing_x = 1
        spacing_y = 1

        start_x = 0
        start_y = self.top

        x = start_x + col_index * (brick_width / 2 + spacing_x)
        y = start_y - row_index * (brick_height / 2 + spacing_y)

        self.position = x, y


class Bricks:
    def __init__(self, **kwargs):
        super(Bricks, self).__init__(**kwargs)
        self.bricks = []

    @log_method
    def load_bricks_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            reader = csv.reader(file)

            for row_index, row in enumerate(reader):
                for col_index, cell in enumerate(row):
                    if cell == "1":
                        brick = Brick()
                        self.bricks.append(brick.set_position(row_index, col_index))
                        self.add_widget(brick)


class PlayerPaddle(Widget, ConcreteObject):
    pass


class GameBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) * 5 + self.pos


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.Bricks = Bricks()

    @log_method
    def serve_ball(self, vel=(0, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player.bounce_ball(self.ball)

        # bounce ball off top, left, or right
        if self.ball.top > self.top:
            self.ball.velocity_y *= -1
        elif self.ball.x < self.x:
            self.ball.velocity_x *= -1
        elif self.ball.right > self.right:
            self.ball.velocity_x *= -1

        # Check collision with the bricks
        for brick in self.bricks:
            brick.bounce_ball(self.ball)
            self.remove_widget(brick)

            # # Adjust ball velocity after collision
            # self.ball.velocity_y *= -1

        # Bounce ball off bottom of the screen
        if self.ball.y < 0:
            self.ball.velocity_y *= -1

        # ball falls to through the bottom
        # if self.ball.y < self.y-50:
        #     logger.info("Ball fell through the bottom")
        #     exit(0)

    def on_touch_move(self, touch):
        if touch.y < self.width / 3:
            self.player.center_x = touch.x

    @log_method
    def start_game(self, *args):
        # self.bricks_grid = GridLayout(cols=8, spacing=10)
        # self.add_widget(self.bricks_grid)
        self.Bricks.load_bricks_from_csv("src/levels/level1.csv")
        self.serve_ball((randint(1, 10), randint(1, 10)))
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def quit_game(self, *args):
        App.get_running_app().stop()


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        # set the orientation and padding of the BoxLayout
        self.orientation = "vertical"
        self.padding = 50

        # add the Game title
        title = Label(text="A BRICKS GAME", font_size=50, size_hint=(1, 0.5))
        self.add_widget(title)

        # add the play button
        play_button = Button(text="PLAY", font_size=30, size_hint=(1, 0.3), background_color=[0, 1, 0, 1])
        play_button.bind(on_release=self.start_game)
        self.add_widget(play_button)

        # add the quit button
        quit_button = Button(text="QUIT", font_size=30, size_hint=(1, 0.2), background_color=[1, 0, 0, 1])
        quit_button.bind(on_release=self.quit_game)
        self.add_widget(quit_button)

    def start_game(self, *args):
        game = Game()
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(game)
        game.start_game()

    def quit_game(self, *args):
        App.get_running_app().stop()


class BricksApp(App):
    def build(self):
        menu = MainMenu()
        return menu


if __name__ == "__main__":
    BricksApp().run()
