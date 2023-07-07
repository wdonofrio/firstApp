from src.decorators import log_method
from src.logging_config import logger
from src.resources import POP_SOUND


class ConcreteObject:
    position = 0, 0

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
