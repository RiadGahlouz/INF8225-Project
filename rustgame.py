import game

from cffi import FFI
ffi = FFI()
ffi.cdef("""
struct BoardState {
    int low;
    int high;
};
struct BoardState move_left(int high, int low);
struct BoardState move_right(int high, int low);
struct BoardState move_up(int high, int low);
struct BoardState move_down(int high, int low);
struct BoardState spawn_tile(int high, int low);
bool is_dead(int high, int low);
""")

C = ffi.dlopen("./impl-2048/target/i686-pc-windows-msvc/debug/impl_2048.dll")

class GameGrid(object):
    def __init__(self):
        self._low = 0x0200_0011
        self._high = 0x4000_0301

    def do_move(self, direction: game.MoveDirection):
        state = None
        if direction == game.MoveDirection.DOWN:
            state = C.move_down(self._high, self._low)
        elif direction == game.MoveDirection.UP:
            state = C.move_up(self._high, self._low)
        elif direction == game.MoveDirection.LEFT:
            state = C.move_left(self._high, self._low)
        elif direction == game.MoveDirection.RIGHT:
            state = C.move_right(self._high, self._low)

        if self._low == state.low and self._high == state.high:
            return # wrong move
        
        state = C.spawn_tile(state.high, state.low)

        if C.is_dead(state.high, state.low):
            state = C.spawn_tile(0, 0)
            state = C.spawn_tile(state.high, state.low)
    
        self._high = state.high
        self._low = state.low

    
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