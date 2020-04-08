from enum import Enum
import random

COLOR_DICT = {
    2: (238, 228, 218),  # Font color: (119, 110, 101)
    4: (237, 224, 200),  # Same font color as 2
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}


class MoveDirection(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


def get_random_grid_element_coords() -> (int, int):
    return random.randint(0, 3), random.randint(0, 3)


def get_color_for_number(number: int) -> (int, int, int):
    if number in COLOR_DICT:
        return COLOR_DICT[number]
    return 204, 192, 179


class GameGrid(object):
    def __init__(self):
        self.elements = [[0 for i in range(4)] for j in range(4)]

        # Spawn 2 elements randomly in the grid. Either a "2" or "4"
        x, y = get_random_grid_element_coords()
        self.elements[x][y] = 2 if random.random() < 0.9 else 4

        while True:
            x2, y2 = get_random_grid_element_coords()
            if x2 != x or y2 != y:
                self.elements[x2][y2] = 2 if random.random() < 0.9 else 4
                break

    def do_move(self, direction: MoveDirection):
        if direction == MoveDirection.BOTTOM:
            self.__move_vertical(1)
        elif direction == MoveDirection.TOP:
            self.__move_vertical(-1)
        elif direction == MoveDirection.LEFT:
            self.__move_horizontal(-1)
        elif direction == MoveDirection.RIGHT:
            self.__move_horizontal(1)

    def __move_horizontal(self, dir_x: int):
        # TODO
        pass

    def __move_vertical(self, dir_y: int):
        # TODO
        pass

    def get_elements(self) -> [[int]]:
        return self.elements
