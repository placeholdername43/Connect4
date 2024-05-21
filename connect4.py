from enum import Enum
from typing import Tuple, TypeAlias, Optional
import numpy as np 
from dataclasses import dataclass

# connect4 - a simple connect 4 game made using functional programming

MAIN_MENU_OPTION = "Enter 1 for Single Player, 2 for Multi Player, or 3 to Exit: "
TOKEN_MENU_OPTION = "Enter R to play as the red token or Y to play as the yellow token: "
TOKEN_PLACEMENT_COLUMN = "What column do you want the token in?, between (1-7): "

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

class BoundedStack: 
    def __init__(self, capacity):
        self.items = []
        self._maxSize = capacity
        assert(capacity >= 0), "not positive"

        try:
            capacity = int(capacity)
        except TypeError as inst:
            print("Error", inst.args)
        except:
            print("error")
        else:
            itemmax = capacity



                        
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


"""
# Bounded Stack



"""




def print_grid(grid: Grid):
    for row in range(5, -1, -1):
        for column in grid:
            cell = column[row] # a cell is a point intersecting a certain row and column
            print(cell if cell is not None else '[ ]', end=' ')
        print(row)
    for i in range(1, 8, 1):
        print(f'{i:^3}', end = ' ')
    print()
    
def prompt_for_token_placement() -> int:
    while True:
        n: int = int(input(TOKEN_PLACEMENT_COLUMN))
        if 1 <= n <= 7:
            return n - 1
        else:
            print("Invalid input, please enter a number between 1-7")



def check_any_empty_cell(c: Column):
    for i in range(len(c)):
        if c[i] == None:
            return i
        return None

def drop_token_in_column(c:Column, t:Token) -> Optional[Column]:
    match check_any_empty_cell(c):
        case None:
            return None
        case i:
            temp = list(c)
            temp[i] = t
            return tuple(temp)
        
def place_new_column_in_grid(grid: Grid, column_idx: int, new_column: Column) -> Grid:
    return grid[:column_idx] + (new_column,) + grid[column_idx + 1:]
        
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



def singleplayer(grid: Grid) -> Grid:
    chosen_token = prompt_for_token_type()
    print_grid(grid)
    chosen_col_idx = prompt_for_token_placement()
    chosen_col = grid[chosen_col_idx]
    new_col = drop_token_in_column(chosen_col, chosen_token)
    if new_col:
        grid = place_new_column_in_grid(grid, chosen_col_idx, new_col)
    else:
        print("Column is full!")
    print_grid(grid)
    return grid

    

def multiplayer():
    pass

def exit():
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
            pass
        case MainMenuOption.Exit:
            pass


def main():
    grid = create_empty_grid()
    while True:
        menu_option = prompt_for_main_menu_input()
        grid = branch_to_game_feature(menu_option, grid)


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