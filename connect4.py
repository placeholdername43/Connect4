from enum import Enum
import sys
from typing import Final, Tuple, TypeAlias, Optional, Union, Callable
from dataclasses import dataclass

MAIN_MENU_MSG: Final[str] = """
Welcome to Connect Four!

What would you like to do?

1. Singleplayer
2. Multiplayer
3. Exit

Enter the number of the option you would like to select (e.g., 1):
"""
TOKEN_MENU_OPTION: Final[str] = "Enter R to play as the red token or Y to play as the yellow token: "
TOKEN_PLACEMENT_COLUMN: Final[str] = "What column do you want the token in?, between (1-7): "
EXIT_CONFIRMATION_MSG: Final[str] = "Are you sure you would like to exit? (enter y/n)"
InputText: TypeAlias = str

class MainMenuOption(Enum):
    SinglePlayer = 1
    MultiPlayer = 2
    Exit = 3
    @staticmethod
    def parse(s: InputText) -> Optional['MainMenuOption']: # this is a forward declaration
        #when python figures out waht the menuoption is, itll come back and give valid returnvalue
        match s.strip().lower():
            case "1" | "singleplayer": return MainMenuOption.SinglePlayer
            case "2" | "multiplayer": return MainMenuOption.MultiPlayer
            case "3" | "exit": return MainMenuOption.Exit
            case _: return None
# we want tokens to be immutable, hence the frozen, both tokens are also equal
@dataclass(eq=True, frozen=True)
class R():
    def __repr__(self) -> str:
        return "R"
    pass

@dataclass(eq=True, frozen=True)
class Y():
    def __repr__(self) -> str:
        return "Y"
    pass


Token: TypeAlias = R | Y 
Cell: TypeAlias = Optional[Token] # define the cell type 
# Another datastructure could be a stack 
Column: TypeAlias = Tuple[Cell, Cell, Cell, Cell, Cell, Cell] # defining a column as a tuple of 6 cells reflecting the 6 high grid of connect 4
Grid: TypeAlias = Tuple[Column, Column, Column, Column, Column, Column, Column] # a grid is therefore a tuple of 7 columns reflecting the 7 high grid of connect4

def prompt_for_input(parse_func: Callable[[str], Optional[MainMenuOption | Token | int]], message: str, err_msg: str) -> Callable[[], MainMenuOption | Token | int]:
    def inner():
        while True:
            match parse_func(input(message)):
                case None:
                    print(err_msg, file=sys.stderr)
                case x:
                    return x
    return inner

def parse_token(s: InputText) -> Optional[Token]:
    match s.lower():
        case "r" | "red" | "1": return R()
        case "y" | "yellow" | "2": return Y()
        case _: return None

def parse_column(s: InputText) -> Optional[int]:
    if s.isdigit() and 1 <= int(s) <= 7:
        return int(s) - 1
    return None

def parse_exit(s: InputText) -> Optional[int]:
    match s.lower():
        case "y" | "yes" | "1": return True
        case "n" | "no" | "2": return False
        case _: return None

prompt_for_token_type = prompt_for_input(parse_token, TOKEN_MENU_OPTION, "ERROR: Invalid input, please select a valid token R/Y")
prompt_for_column = prompt_for_input(parse_column, TOKEN_PLACEMENT_COLUMN, "ERROR: Invalid input, please select a column between 1-7")
prompt_for_main_menu_input = prompt_for_input(MainMenuOption.parse, MAIN_MENU_MSG, "ERROR: not a valid menu option")
prompt_for_exit_confirmation = prompt_for_input(parse_exit, EXIT_CONFIRMATION_MSG, "ERROR: Please input yes to exit the game or no to stay")

def create_empty_grid() -> Grid:
    c: Column = (None, None, None, None, None, None)
    g: Grid = (c, c, c, c, c, c, c)
    return g

def print_grid(grid: Grid) -> None:  # change to render and seperate print
    for row in range(5, -1, -1):
        print("|", end="")
        for column in grid:
            cell = column[row]
            print(f" {cell if cell is not None else ' '} ", end="|")
        print()
    print(" " + "   ".join(map(str, range(1, 8))))

def check_any_empty_cell(c: Column) -> Optional[int]:
    for i in range(len(c)):
        if c[i] is None:
            return i
    return None

# change to list comprehension
def check_direction(grid: Grid, start_row, start_col, direction_row, direction_col, token) -> int:
    count = 0
    row = start_row
    col = start_col
    while 0 <= row < 6 and 0 <= col < 7 and grid[col][row] == token:
        count += 1
        row += direction_row
        col += direction_col
    return count

def check_for_win(grid: Grid, token: Token) -> bool:
    for col in range(7):
        for row in range(6):
            if grid[col][row] == token:
                if (check_direction(grid, row, col, 1, 0, token) >= 4 or  # vertical 
                    check_direction(grid, row, col, 0, 1, token) >= 4 or  # horizontal 
                    check_direction(grid, row, col, 1, 1, token) >= 4 or  # diagonal negative right
                    check_direction(grid, row, col, 1, -1,token) >= 4):  # diagonal positive righ
                    return True
    return False

def drop_token_in_column(c: Column, t: Token) -> Optional[Column]:
    match check_any_empty_cell(c):
        case None:
            return None
        case i:
            newColumn = list(c)
            newColumn[i] = t
            return tuple(newColumn)

def place_new_column_in_grid(grid: Grid, columnIdx: int, newColumn: Column) -> Grid:
    return grid[:columnIdx] + (newColumn,) + grid[columnIdx + 1:]

def check_grid_full(grid: Grid) -> bool:
    return not any(check_any_empty_cell(col) is not None for col in grid)

def turn_by_turn(grid: Grid, playerIdx: int, tokens: Tuple[Token, Token]) -> Tuple[Grid, bool]:
    print_grid(grid)
    print(f"Player {playerIdx + 1}'s turn ({tokens[playerIdx]}):")
    
    while True:
        columnIdx = prompt_for_column()
        newColumn = drop_token_in_column(grid[columnIdx], tokens[playerIdx])
        if newColumn is not None:
            break
        else:
            print("Column is full! Try a different column.")
    
    newGrid = place_new_column_in_grid(grid, columnIdx, newColumn)

    if check_for_win(newGrid, tokens[playerIdx]):
        print_grid(newGrid)
        print(f"Player {playerIdx + 1} ({tokens[playerIdx]}) wins!")
        return newGrid, True
        
    if check_grid_full(newGrid):
        print_grid(newGrid)
        print("The game is a draw!")
        return newGrid, True
    
    return newGrid, False

def game_loop(grid: Grid, playerIdx: int, tokens: Tuple[Token, Token]) -> None:
    new_grid, game_over = turn_by_turn(grid, playerIdx, tokens)
    if not game_over:
        game_loop(new_grid, 1 - playerIdx, tokens)

def singleplayer():
    print("Singleplayer placeholder ")

def multiplayer() -> None:
    print("Player 1: Select a token")
    player1_token : Token = prompt_for_token_type()
    if isinstance(player1_token, R):
        player2_token = Y()
    else:
        player2_token = R()
    tokens = (player1_token, player2_token)
    grid = create_empty_grid()
    game_loop(grid, 0, tokens)

def exit_game() -> None:
    confirmation = prompt_for_exit_confirmation()
    if confirmation:
        print("Thank you for playing Connect Four. Goodbye!")
        sys.exit(0)

def branch_to_game_feature(opt: MainMenuOption) -> None:
    match opt:
        case MainMenuOption.SinglePlayer:
            singleplayer()
        case MainMenuOption.MultiPlayer:
            multiplayer()
        case MainMenuOption.Exit:
            exit_game()

def main():
    while True:
        menu_option = prompt_for_main_menu_input()
        branch_to_game_feature(menu_option)

if __name__ == "__main__":
    main()
