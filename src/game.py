from random import randint

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.vector import Vector


from src.objects import ConcreteObject
from src.bricks import Bricks
from src.decorators import log_method


class PlayerPaddle(ConcreteObject):
    pass


class GameBall(Widget):
    def move(self):
        self.pos = Vector(*self.velocity) * 5 + self.pos


class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Bricks = Bricks()

    def on_touch_move(self, touch):
        if touch.y < self.width / 3:
            self.player.center_x = touch.x

    @log_method
    def serve_ball(self, vel=(0, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update_bricks(self, ball):
        bricks_to_remove = []

        brick_units = self.Bricks.get_bricks()
        for brick in brick_units:
            brick.bounce_obj(ball)
            if brick.collides_with(ball):
                bricks_to_remove.append(brick)

        for brick in bricks_to_remove:
            self.remove_widget(brick)
            self.Bricks.remove(brick)

    def bounce_off_walls(self, ball):
        # bounce ball off top, left, or right
        velocity_x, velocity_y = self.ball.velocity
        if ball.top > self.top:
            velocity_y *= -1
        elif ball.x < self.x or ball.right > self.right:
            velocity_x *= -1
        # Bounce ball off bottom of the screen
        if ball.y < 0:
            velocity_y *= -1

        ball.velocity = velocity_x, velocity_y

    def game_over(self):
        # ball falls to through the bottom
        if self.ball.y < self.y - 50:
            exit(0)

    def update(self, dt):
        self.ball.move()

        self.bounce_off_walls(self.ball)
        self.player.bounce_obj(self.ball)

        # Check collision with the bricks
        self.update_bricks(self.ball)

    @log_method
    def start_game(self, *args):
        self.Bricks.load_bricks_from_csv("src/levels/level1.csv")
        self.serve_ball((randint(-1, 1), randint(-1, 1)))
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def quit_game(self, *args):
        App.get_running_app().stop()
