from kivy.uix.widget import Widget
from kivy.vector import Vector

from src.resources import POP_SOUND


class ConcreteObject(Widget):
    position = 0, 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collides_with(self, obj) -> bool:
        return self.collide_widget(obj)

    def bounce_obj(self, obj, velocity=1.0):
        if not self.collide_widget(obj):
            return
        offset = obj.center_y - self.center_y
        velocity_x, velocity_y = obj.velocity

        # Adjust the velocity based on the collision position
        if offset > 0:
            # Ball hits the top part of the paddle
            new_velocity = Vector(-velocity_x, abs(velocity_y))
        else:
            # Ball hits the bottom part of the paddle
            new_velocity = Vector(-velocity_x, -abs(velocity_y))

        # Apply speedup and set the new velocity
        obj.velocity = velocity * new_velocity
        POP_SOUND.play()
