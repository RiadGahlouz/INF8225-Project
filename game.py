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
        self.elements[x][y] = random.choice([2, 4])
        x, y = get_random_grid_element_coords()
        self.elements[x][y] = random.choice([2, 4])

    def do_move(self, direction: MoveDirection):
        pass

    def get_elements(self) -> [[int]]:
        return self.elements
