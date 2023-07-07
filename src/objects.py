from kivy.uix.widget import Widget

from src.logging_config import logger
from src.resources import POP_SOUND


class ConcreteObject(Widget):
    position = 0, 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collides_with(self, obj) -> bool:
        return self.collide_widget(obj)

    def bounce_obj(self, obj, velocity=1.0):
        if self.collide_widget(obj):
            offset_x = (obj.center_x - self.center_x) / (self.width / 2)
            offset_y = (obj.center_y - self.center_y) / (self.height / 2)
            logger.info(f"{offset_x}, {offset_y}")
            # Adjust the offset based on which corner the obj collides with
            if offset_x > 0:
                offset_x = 1 - offset_x
            else:
                offset_x = -1 - offset_x

            if offset_y > 0:
                offset_y = 1 - offset_y
            else:
                offset_y = -1 - offset_y

            obj.velocity = (
                obj.velocity[0] * velocity + offset_x,
                obj.velocity[1] * velocity + offset_y,
            )
            POP_SOUND.play()
