from random import randint

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

from src.bricks import Bricks
from src.decorators import log_method


class Game(Widget):
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
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

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player.bounce_obj(self.ball)

        # bounce ball off top, left, or right
        if self.ball.top > self.top:
            self.ball.velocity_y *= -1
        elif self.ball.x < self.x:
            self.ball.velocity_x *= -1
        elif self.ball.right > self.right:
            self.ball.velocity_x *= -1

        # Check collision with the bricks
        self.update_bricks(self.ball)

        # Bounce ball off bottom of the screen
        if self.ball.y < 0:
            self.ball.velocity_y *= -1

        # ball falls to through the bottom
        # if self.ball.y < self.y-50:
        #     logger.info("Ball fell through the bottom")
        #     exit(0)

    @log_method
    def start_game(self, *args):
        self.Bricks.load_bricks_from_csv("src/levels/level1.csv")
        self.serve_ball((randint(1, 10), randint(1, 10)))
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def quit_game(self, *args):
        App.get_running_app().stop()
