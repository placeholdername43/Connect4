from enum import Enum
from typing import Final, Tuple, TypeAlias, Optional
import numpy as np 
from dataclasses import dataclass

# connect4 - a simple connect 4 game made using functional programming

MAIN_MENU_OPTION: Final[str] = "Enter 1 for Single Player, 2 for Multi Player, or 3 to Exit: "
TOKEN_MENU_OPTION: Final[str] = "Enter R to play as the red token or Y to play as the yellow token: "
TOKEN_PLACEMENT_COLUMN: Final[str] = "What column do you want the token in?, between (1-7): "

InputText: TypeAlias = str

class MainMenuOption(Enum):
    SinglePlayer = 1
    MultiPlayer = 2
    Exit = 3
    @staticmethod
    def parse(s: InputText) -> Optional['MainMenuOption']: # this is a forward declaration
        #when python figures out waht the menuoption is, itll come back and give valid returnvalues
        match s.strip().lower():
            case "1" | "singleplayer": return MainMenuOption.SinglePlayer
            case "2" | "multiplayer": return MainMenuOption.MultiPlayer
            case "3" | "exit": return MainMenuOption.Exit
            case _: return None
                      
# we want tokens to be immutable, hence the frozen, both tokens are also equal
@dataclass(eq = True, frozen = True) 
class R():
    def __repr__(self) -> str:
        return "R"
    pass
@dataclass(eq= True, frozen = True)
class Y():
    def __repr__(self) -> str:
        return "Y"
    pass

Token: TypeAlias = R | Y 


Cell: TypeAlias = Optional[Token] # define the cell type 
# Another datastructure could be a stack 
Column: TypeAlias = Tuple[Cell, Cell, Cell, Cell, Cell, Cell] # defining a column as a tuple of 6 cells reflecting the 6 high grid of connect 4
Grid: TypeAlias = Tuple[Column, Column, Column, Column, Column, Column, Column] # a grid is therefore a tuple of 7 columns reflecting the 7 high grid of connect4

def create_empty_grid() -> Grid:
    return tuple(tuple(None for _ in range(6)) for _ in range(7))

def print_grid(grid: Grid):
    for row in range(5, -1, -1):
        print("|", end="")
        for column in grid:
            cell = column[row]  # A cell is a point intersecting a certain row and column
            print(f" {cell if cell is not None else ' '} ", end="|")
        print()
    print(" " + "   ".join(map(str, range(1, 8))))
    
def prompt_for_token_placement() -> int:
    while True:
        n = input(TOKEN_PLACEMENT_COLUMN)
        match n:
            case _ if n.isdigit() and 1 <= int(n) <= 7:
                return int(n) - 1
            case _:
                print("Invalid input, please enter a number between 1-7")

def check_any_empty_cell(c: Column) -> Optional[int]:
    for i in range(len(c)):
        if c[i] is None:
            return i
    return None

def check_for_win(g: Grid, t: Token) -> bool:
    # a win can be horizontal, diagonal, vertical
    # how will i check thru the grid in all directions to determine a win
    # potentially a function to check in each direction?
    return True

def drop_token_in_column(c:Column, t:Token) -> Optional[Column]:
    match check_any_empty_cell(c):
        case None:
            return None
        case i:
            newColumn = list(c)
            newColumn[i] = t
            return tuple(newColumn)
        
def place_new_column_in_grid(grid: Grid, columnIdx: int, newColumn: Column) -> Grid:
    return grid[:columnIdx] + (newColumn,) + grid[columnIdx + 1:]
        
def prompt_for_token_type() -> Optional[Token]:
    while True:
        s: str = input(TOKEN_MENU_OPTION)
        match s.lower():
            case "r" | "red" | "1":
                return R()
            case "y" | "yellow" | "2":
                return Y()
            case _:
                return None

def check_grid_full(grid: Grid) -> bool:
    return not any(check_any_empty_cell(col) is not None for col in grid)

def turn_by_turn(grid: Grid, playerIdx: int, tokens: Tuple[Token, Token]) -> Tuple[Grid, bool]:
    print_grid(grid)
    print(f"Player {playerIdx + 1}'s turn ({tokens[playerIdx]}):")
    columnIdx = prompt_for_token_placement()
    newColumn = drop_token_in_column(grid[columnIdx], tokens[playerIdx])
    if newColumn is None:
        print("Column is full! Try a different column.")
        return grid, False
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

def game_loop(grid: Grid, playerIdx: int, tokens: Tuple[Token, Token]):
    new_grid, game_over = turn_by_turn(grid, playerIdx, tokens)
    if not game_over:
        game_loop(new_grid, 1 - playerIdx, tokens)

def singleplayer():
    print("Singleplayer placeholder.")

def multiplayer():
    grid = create_empty_grid()
    tokens = (R(), Y())
    game_loop(grid, 0, tokens)

def exit_game():
    print("Are you sure you would like to quit? Y/N")
    print("TODO: Need to add quit prompt declaratively ")
    quit()

def prompt_for_main_menu_input():
    while True:
        match MainMenuOption.parse(input(MAIN_MENU_OPTION)):
            case x if type(x) == MainMenuOption:
                return x
            case _:
                print("ERROR: not a valid menu option")

def branch_to_game_feature(opt: MainMenuOption):
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
        grid = branch_to_game_feature(menu_option)


if __name__ == "__main__":
    main()

"""
    for row in range(5, -1, -1):
        for column in grid:
            cell = column[row] # a cell is a point intersecting a certain row and column
            print(cell if cell is not None else '[ ]', end=' ')
        print(row)"""


"""
Row: TypeAlias = Tuple[Cell,Cell,Cell]
Grid: TypeAlias = Tuple[Row,Row,Row]

exampleRow : Row(None,None,None)
exampleGrid : Grid =  """



"""def parse_Token(s: InputText) -> Optional[Token]:
        match s.lower():
            case "r" | "red" | "1":
                print("Red Token Selected!")
                return R()
            case "y" | "yellow" | "2":
                print("Yellow Token Selected!")
                return Y()
            case _:
                print("Invalid input pick a correct token (R/Y)")
                return None

def prompt_for_token():
    while True:
        match parse_Token(input(TOKEN_MENU_OPTION)):
            case _ as Token:
                return Token"""