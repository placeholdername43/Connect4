from enum import Enum
from typing import Tuple, TypeAlias, Optional
import numpy as np 
from dataclasses import dataclass

# connect4 - a simple connect 4 game made using functional programming
"""
plan

1. allow a player to chose multiplayer or singleplayer thru the commandline
2. if multiplayer, allow 2 players to play
3. if singleplayer, allow the player to play against the computer
    3.1 the computer should use a minimax algorithm to determine the best move
    3.2 the singleplayer function should call another function with the acc game logic
4. allow the player to chose the difficulty of the computer and/or auto tune it
5. represent the two players using x/o
6. reprsent the board using a matrix
7. allow the player to chose a column to place their piece
8. remember to consider the gravity of the pieces, they must fall to the bottom
9. when a piece is placed, check if the player has won
10. if the player has won, end the game and display the winner
11. if the player has not won, switch to the next player
12. if the board is full and no player has won, end the game and display a draw
13. allow the player to play again or quit

"""
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
grid: Grid = list(list(None for _ in range(6)) for _ in range(7)) # the grid is therefore created as a first having empty values in each row, as no tokens are placed initially



def print_grid(grid: Grid):
    for row in range(5, -1, -1):
        for column in grid:
            cell = column[row] # a cell is a point intersecting a certain row and column
            print(cell if cell is not None else '[ ]', end=' ')
        print(row)
    for i in range(1, 8, 1):
        print(f'{i:^3}', end = ' ')
    
def prompt_for_token_placement() -> int:
    while True:
        n: int = int(input(TOKEN_PLACEMENT_COLUMN))
        if 1 <= n <= 6:
            return n
        else:
            print("Invalid input, please enter a number between 1-7")

def provide_column_specified_by_user_to_place_in(n):
    return grid[n-1]

def check_any_empty_cell(c: Column):
    for i in range(0,len (c) - 1):
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
            c = tuple(temp)
            c = Column
            return c
        
def place_new_column_in_grid(columnIdx, newColumn: Column) -> Grid:
    print(grid[columnIdx])
    grid[columnIdx] 
    return grid
        

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

def singleplayer():
    prompt_for_main_menu_input()
    ChosenToken = prompt_for_token_type()
    chosenColIdx = prompt_for_token_placement()
    chosenCol = provide_column_specified_by_user_to_place_in(chosenColIdx)
    newCol = drop_token_in_column(chosenCol, ChosenToken)
    place_new_column_in_grid(chosenColIdx, newCol)
    print_grid(grid)
    

    

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
    """prompt for menu option
    then branch to a feature"""
    match opt:
        case MainMenuOption.SinglePlayer:
            singleplayer()
        case MainMenuOption.MultiPlayer:
            print("Multi Player")
        case MainMenuOption.Exit:
            print("Goodbye")
            return
        
    
if __name__ == "__main__":
    branch_to_game_feature(prompt_for_main_menu_input())