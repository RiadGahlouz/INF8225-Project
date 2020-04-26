#[repr(C)]
pub struct BoardState {
    pub low: u32,
    pub high: u32,
}

impl Into<u64> for BoardState {
    fn into(self) -> u64 {
        let high = self.high as u64;
        let low = self.low as u64;

        (high << 32u64) + low
    }
}

impl Into<BoardState> for u64 {
    fn into(self) -> BoardState {
        BoardState {
            low: (self & 0xFFFFFFFF) as u32,
            high: ((self >> 32) & 0xFFFFFFFF) as u32
        }
    }
}

#[no_mangle]
pub extern "C" fn move_dir(high: u32, low: u32, direction: u8) -> BoardState {
    let directions: Vec<tfe::Direction> = vec![
        tfe::Direction::Left,
        tfe::Direction::Up,
        tfe::Direction::Right,
        tfe::Direction::Down,
    ];
    tfe::Game::execute(BoardState{high, low}.into(), &directions[direction as usize]).into()
}

#[no_mangle]
pub extern "C" fn move_left(high: u32, low: u32) -> BoardState {
    tfe::Game::move_left(BoardState { high, low }.into()).into()
}

#[no_mangle]
pub extern "C" fn move_right(high: u32, low: u32) -> BoardState {
    tfe::Game::move_right(BoardState { high, low }.into()).into()
}

#[no_mangle]
pub extern "C" fn move_up(high: u32, low: u32) -> BoardState {
    tfe::Game::move_up(BoardState { high, low }.into()).into()
}

#[no_mangle]
pub extern "C" fn move_down(high: u32, low: u32) -> BoardState {
    tfe::Game::move_down(BoardState { high, low }.into()).into()
}

#[no_mangle]
pub extern "C" fn spawn_tile(high: u32, low: u32) -> BoardState {
    let board = BoardState { high, low }.into();
    (tfe::Game::spawn_tile(board) | board).into()
}
#[no_mangle]
pub extern "C" fn is_dead(high: u32, low: u32) -> bool {
    let board = BoardState { high, low }.into();

    (tfe::Game::move_left(board) == board) && (tfe::Game::move_right(board) == board) &&
    (tfe::Game::move_up(board) == board) && (tfe::Game::move_down(board) == board)
}