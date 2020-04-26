import game

from cffi import FFI
ffi = FFI()
ffi.cdef("""
struct BoardState {
    int low;
    int high;
};
struct BoardState move_dir(int high, int low, unsigned char direction);
struct BoardState spawn_tile(int high, int low);
bool is_dead(int high, int low);
""")

C = ffi.dlopen("./impl-2048/target/i686-pc-windows-msvc/release/impl_2048.dll")

class GameGrid(object):
    def __init__(self):
        state = C.spawn_tile(0x0000_0000, 0x0000_0000)
        state = C.spawn_tile(state.high, state.low)
        self._low = state.low
        self._high = state.high
        self._old_low = self._low
        self._old_high = self._high

    def get_fitness(self, gen):
        tiles = []
        for e in self.elements:
            tiles += e
        
        return sum(tiles)

    def do_move(self, direction: game.MoveDirection):
        self._old_low = self._low
        self._old_high = self._high
        state = None
        state = C.move_dir(self._high, self._low, int(direction))

        if self._low == state.low and self._high == state.high:
            return False# wrong move
        
        state = C.spawn_tile(state.high, state.low)
    
        self._high = state.high
        self._low = state.low

        return True

    def is_game_over(self) -> bool:
        return C.is_dead(self._high, self._low)

    
    def get_elements(self) -> [[int]]:
        elements = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        for y in range(0, 4):
            for x in range(0, 4):
                source = self._high if y >= 2 else self._low
                decal = y - 2 if y >= 2 else y
                value = (source >> (x * 4 + decal * 16)) & 0xF

                elements[3 - y][3 - x] = 0 if value == 0 else 2 ** value
        
        return elements

    @property
    def elements(self):
        return self.get_elements()
        
    @property
    def oldElements(self):
        elements = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        for y in range(0, 4):
            for x in range(0, 4):
                source = self._old_high if y >= 2 else self._old_low
                decal = y - 2 if y >= 2 else y
                value = (source >> (x * 4 + decal * 16)) & 0xF

                elements[3 - y][3 - x] = 0 if value == 0 else 2 ** value
        
        return elements