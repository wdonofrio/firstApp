import pytest
from unittest.mock import Mock, patch

from kivy.tests.common import GraphicUnitTest

from src.game import Game, GameBall, PlayerPaddle
from src.bricks import Brick


class GameTestCase(GraphicUnitTest):
    @pytest.mark.skip(reason="Not setup")
    def test_serve_ball(self):
        game = Game()
        game.size = (800, 600)
        game.serve_ball((2, 3))
        ball = game.ball
        self.assertEqual(ball.velocity, (2, 3))
        # expected_center = (game.center_x - ball.width / 2, game.center_y - ball.height / 2)
        # self.assertEqual(ball.center, expected_center)

    @pytest.mark.skip(reason="Not setup")
    def test_update_bricks(self):
        game = Game()
        brick1 = Brick(pos=(100, 100), size=(50, 50))
        brick2 = Brick(pos=(200, 200), size=(50, 50))
        game.add_widget(brick1)
        game.add_widget(brick2)
        ball = GameBall(pos=(150, 150), size=(20, 20))
        game.update_bricks(ball)
        self.assertEqual(game.Bricks.get_bricks(), [brick1, brick2])
        ball.pos = (110, 110)
        game.update_bricks(ball)
        self.assertEqual(game.Bricks.get_bricks(), [brick2])

    def test_bounce_off_walls(self):
        ball = GameBall()
        ball.pos = (100, 100)
        ball.velocity = (1, 1)

        # Ball hits the top wall
        ball.top = ball.parent.height + 1  # Set top coordinate to simulate top wall collision
        ball.bounce_off_walls()
        assert ball.velocity == (1, -1)

        # # Ball hits the left wall
        # ball.x = 0
        # ball.right = 20  # Set right coordinate to simulate left wall collision
        # ball.parent = None  # Set parent to None to simulate left wall collision
        # ball.bounce_off_walls()
        # assert ball.velocity == (-1, -1)

        # # Ball hits the right wall
        # ball.right = 800
        # ball.x = 780  # Set x coordinate to simulate right wall collision
        # ball.parent = None  # Set parent to None to simulate right wall collision
        # ball.bounce_off_walls()
        # assert ball.velocity == (-1, -1)

        # # Ball hits the bottom wall
        # ball.y = 0
        # ball.top = 20  # Set top coordinate to simulate bottom wall collision
        # ball.parent = None  # Set parent to None to simulate bottom wall collision
        # ball.bounce_off_walls()
        # assert ball.velocity == (-1, 1)

    @pytest.mark.skip(reason="Not setup")
    def test_update(self):
        game = Game()
        game.ball = GameBall(pos=(100, 100), size=(20, 20), velocity=(1, -1))
        game.player = PlayerPaddle(pos=(200, 200), size=(100, 20))
        game.update(1)
        ball = game.ball
        player = game.player
        assert ball.pos == (101, 99)
        assert not player.bounced

    def test_quit_game(self):
        game = Game()
        app = Mock()
        with patch("kivy.app.App.get_running_app", return_value=app):
            game.quit_game()
            app.stop.assert_called_once()

    # def test_start_game(self):
    #     game = Game()
    #     game.size = (800, 600)
    #     game.Bricks = Bricks()
    #     game.ball = GameBall()
    #     game.player = PlayerPaddle()
    #     Clock.schedule_interval(game.update, 1.0 / 60.0)
    #     game.start_game()
