from csv import reader
from typing import List

from kivy.uix.widget import Widget
from src.objects import ConcreteObject

from src.decorators import log_method


class Brick(Widget, ConcreteObject):
    def __init__(self, **kwargs):
        super(Brick, self).__init__(**kwargs)
        self.width, self.height = 30, 30
        self.size = (self.width, self.height)

    def set_position(self, row_index, col_index):
        brick_width, brick_height = self.size
        spacing_x = 1
        spacing_y = 1

        start_x = 0
        start_y = self.top

        x = start_x + col_index * (brick_width / 2 + spacing_x)
        y = start_y - row_index * (brick_height / 2 + spacing_y)

        self.position = x, y


class Bricks(Widget):
    def __init__(self, **kwargs):
        super(Bricks, self).__init__(**kwargs)
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
