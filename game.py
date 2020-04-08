from enum import Enum
import random


class MoveDirection(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3


def get_random_grid_element_coords() -> (int, int):
    return random.randint(0, 3), random.randint(0, 3)


class GameGrid(object):
    def __init__(self):
        self.elements = [[0 for i in range(4)] for j in range(4)]

        # Spawn 2 elements randomly in the grid. Either a "2" or "4"
        x, y = get_random_grid_element_coords()
        self.elements[x][y] = random.choice([2, 4])  # TODO: Make it 90% chance to be a 2 (original game)
        x, y = get_random_grid_element_coords()
        self.elements[x][y] = random.choice([2, 4])

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
