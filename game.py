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
    UP = 1
    RIGHT = 2
    DOWN = 3


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
        self.elements[y][x] = 2 if random.random() < 0.9 else 4

        while True:
            x2, y2 = get_random_grid_element_coords()
            if x2 != x or y2 != y:
                self.elements[y2][x2] = 2 if random.random() < 0.9 else 4
                break

    def do_move(self, direction: MoveDirection):
        if direction == MoveDirection.DOWN:
            self.__move_vertical(1)
        elif direction == MoveDirection.UP:
            self.__move_vertical(-1)
        elif direction == MoveDirection.LEFT:
            self.__move_horizontal(-1)
        elif direction == MoveDirection.RIGHT:
            self.__move_horizontal(1)
        # TODO: Spawn a new element (I think it's 50% chance 2, 50% chances 4)

    def __move_horizontal(self, dir_x: int):
        # Idea: When we move horiszontally, we have 4 independent rows.
        # Each row moves exacly the same way, so they can be processed in //

        # Row index corresponds to the y coord in our array
        rows = [
            self.elements[0],
            self.elements[1],
            self.elements[2],
            self.elements[3],
        ]

        for row in rows:
            # Always move towards 0, the row will be flipped if the dir is negative
            for i in range(1, 4):
                if row[i] == 0:
                    continue  # We can't move a non-existing element
                for target in range(i - 1, -1, -1):
                    print(f"Attempting to move {i} to {target}")
                # If we reach here
            pass

        self.elements[0] = rows[0]
        self.elements[1] = rows[1]
        self.elements[2] = rows[2]
        self.elements[3] = rows[3]
        pass

    def __move_vertical(self, dir_y: int):
        # Step 1: Merge tiles
        # if we move up, we start from row 0
        # if we move down, we start from row 3
        #
        # if elem[y][x] == elem[y - dir_y][x] # Go against the direction for lookup
        #   elem[y][x] *= 2
        #   elem[y + dir_y][x] = 0

        def move_tiles():
            for x in range(len(self.elements[0])):
                col = []
                rng2 = range(0, len(self.elements))
                if dir_y == 1:
                    rng2 = reversed(rng2)
                rng2 = [k for k in rng2]
                for y in rng2:
                    if self.elements[y][x] != 0:
                        col.append(self.elements[y][x])
                        self.elements[y][x] = 0
                # print(f"Column {x}: {col}")

                for y in rng2:
                    # print(f"Placing element at {y}")
                    if len(col) == 0:
                        break
                    self.elements[y][x] = col.pop()

        move_tiles()

        rng = range(0, len(self.elements))
        if dir_y == 1:
            rng = reversed(rng)
        rng = [x for x in rng][:-1]

        for y in rng:
            for x in range(len(self.elements[y])):
                # Go against the direction for lookup
                # print((x,y))
                if self.elements[y][x] == self.elements[y - dir_y][x]:
                    self.elements[y][x] *= 2
                    self.elements[y - dir_y][x] = 0

        move_tiles()

    def get_elements(self) -> [[int]]:
        return self.elements
