from enum import Enum
import random
import statistics
import math
import copy

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
        self.oldElements = copy.deepcopy(self.elements)

        self.score = 0

    def get_fitness(self, gen):
        tiles = []
        for e in self.elements:
            tiles += e

        return max(tiles)
        

    def get_total_score(self):
        score = 0
        r_W = 1.0
        for r in self.elements:
            score += sum( list(filter(lambda a: a > 4, r))) /r_W
            r_W -= 0.2

        return score

    def get_bigest_tile_scoring(self):
        tiles = []
        for e in self.elements:
            tiles += e
        return max(tiles) / statistics.mean(tiles)

    def get_highscore(self): 
        tiles = []
        for e in self.elements:
            tiles += e

        return max(tiles) 

    def do_move(self, direction: MoveDirection):
        self.oldElements = copy.deepcopy(self.elements)
        if direction == MoveDirection.DOWN:
            self.__move_vertical(1)
        elif direction == MoveDirection.UP:
            self.__move_vertical(-1)
        elif direction == MoveDirection.LEFT:
            self.__move_horizontal(-1)
        elif direction == MoveDirection.RIGHT:
            self.__move_horizontal(1)

        if self.oldElements == self.elements:  # No move has been performed
            return False

        # TODO: Spawn a new element (I think it's 50% chance 2, 50% chances 4)
        number_to_spawn = 2  # TODO Allow spawning 4s

        number_of_zeros = 0
        for row in self.elements:
            for item in row:
                if item == 0:
                    number_of_zeros += 1
        if number_of_zeros != 0:
            while True:
                x = random.randrange(0, 4)
                y = random.randrange(0, 4)
                if self.elements[y][x] == 0:
                    self.elements[y][x] = number_to_spawn
                    break
        else:
            pass  # TODO : perdre la partie
        return True


    def __move_horizontal(self, dir_x: int):

        def move_tiles():
            for yh in range(0, len(self.elements)):
                tmp =  list(filter(lambda a: a != 0, self.elements[yh]))
                missing_zero = [0] * (len(self.elements) - len(tmp))
                self.elements[yh] = tmp + missing_zero if  dir_x == -1 else  missing_zero + tmp

        move_tiles()

        rng = range(0, len(self.elements))
        if dir_x == 1:
            rng = reversed(rng)
        rng = [k for k in rng][:-1]

        for xh in (rng):
            for yh in range(len(self.elements[0])):
                if self.elements[yh][xh] != 0 and self.elements[yh][xh] == self.elements[yh][ xh - dir_x]:
                    # print((xh,yh), [self.elements[yh][xh] ], " =? ", (xh-dir_x,yh),[self.elements[yh][ xh - dir_x]  ] )
                    self.elements[yh][xh] *= 2
                    self.elements[yh][xh - dir_x] = 0

                    self.score += self.elements[yh][xh]

        move_tiles()

    def __move_vertical(self, dir_y: int):
        def move_tiles():
            for xv in range(len(self.elements)):
                rng2 = range(0, len(self.elements))
                if dir_y == 1:
                    rng2 = reversed(rng2)
                rng2 = [k for k in rng2]
                for yv, r in enumerate(rng2):
                    if self.elements[r][xv] != 0: continue

                    for yyv in rng2[yv:]:
                        if self.elements[yyv][xv] != 0: 
                            self.elements[r][xv] = self.elements[yyv][xv]
                            self.elements[yyv][xv] = 0
                            break


        move_tiles()

        rng = range(0, len(self.elements))
        if dir_y == 1:
            rng = reversed(rng)
        rng = [k_ for k_ in rng][:-1]

        for yv in (rng):
            for xv in range(len(self.elements[yv])):
                # Go against the direction for lookup
                if self.elements[yv][xv] != 0 and self.elements[yv][xv] == self.elements[yv - dir_y][xv]:
                    # print((xv,yv), [self.elements[yv][xv] ], " =? ", (xv,yv-dir_y), [self.elements[yv - dir_y][xv]])
                    self.elements[yv][xv] *= 2
                    self.elements[yv - dir_y][xv] = 0

                    self.score += self.elements[yv][xv]


        move_tiles()

    def is_game_over(self) -> bool:
        for y_go, row in enumerate(self.elements):
            for x_go, col in enumerate(row):
                # Check value
                val = self.elements[y_go][x_go]
                if val == 0:
                    return False

                # Check surroundings
                if (x_go > 0 and self.elements[y_go][x_go - 1] == val) \
                        or (x_go < len(self.elements) - 1 and self.elements[y_go][x_go + 1] == val) \
                        or (y_go > 0 and self.elements[y_go - 1][x_go] == val) \
                        or (y_go < len(self.elements) - 1 and self.elements[y_go + 1][x_go] == val):
                    return False
        return True

    def get_elements(self) -> [[int]]:
        return self.elements

