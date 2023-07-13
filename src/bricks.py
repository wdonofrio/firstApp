from csv import reader
from typing import List

from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

from src.objects import ConcreteObject
from src.decorators import log_method


class Brick(ConcreteObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.radius = [Window.width * 0.01, Window.width * 0.01, Window.width * 0.01, Window.width * 0.01]
        self.rectangle = RoundedRectangle(radius=self.radius)
        self.size_hint = (None, None)  # Remove the size_hint property
        self.width = Window.width * 0.03
        self.height = Window.width * 0.03
        self.size = (self.width, self.height)
        self.canvas.add(self.rectangle)
        with self.canvas.before:
            Color(1, 1, 1)

    def set_position(self, row_index, col_index):
        brick_width, brick_height = self.size
        spacing_x = Window.width * 0.001
        spacing_y = Window.width * 0.001

        start_x = 0
        start_y = 0

        x = start_x + col_index * (brick_width / 2 + spacing_x)
        y = start_y - row_index * (brick_height / 2 + spacing_y)

        self.pos = x, y

    def on_pos(self, *args):
        self.rectangle.pos = self.pos

    def on_size(self, *args):
        self.rectangle.size = self.size


class Bricks(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bricks = []

    def add(self, brick: Brick) -> None:
        self.bricks.append(brick)

    def remove(self, brick: Brick) -> None:
        self.bricks.remove(brick)

    def get_bricks(self) -> List[Brick]:
        return self.bricks

    @log_method
    def load_bricks_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            file_reader = reader(file)

            for row_index, row in enumerate(file_reader):
                for col_index, cell in enumerate(row):
                    if cell == "1":
                        brick = Brick()
                        brick.set_position(row_index, col_index)
                        self.add(brick)
                        self.add_widget(brick)
