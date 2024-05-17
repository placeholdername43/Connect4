from enum import Enum
from typing import TypeAlias, Optional
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

"""Cell: TypeAlias = Optional[Token]
Row: TypeAlias = Tuple[Cell,Cell,Cell]
Grid: TypeAlias = Tuple[Row,Row,Row]

exampleRow : Row(None,None,None)
exampleGrid : Grid =  """

def prompt_for_main_menu():
    while True:
        match MainMenuOption.parse(input(MAIN_MENU_OPTION)):
            case MainMenuOption.SinglePlayer:
                singleplayer()
            case MainMenuOption.MultiPlayer:
                print("Multi Player")
            case MainMenuOption.Exit:
                print("Goodbye")
                exit()
            case _:
                print("Invalid input. Please try again.")

def parse_Token(s: InputText) -> Optional[Token]:
        match s.lower():
            case "r" | "red" | "1":
                print("Red Token Selected!")
                return R()
            case "y" | "yellow" | "2":
                print("Yellow Token Selected!")
                return Y()
            case _:
                print("Invalid input pick a correct token (R/Y)")

def prompt_for_token():
    while True:
        match parse_Token(input(TOKEN_MENU_OPTION)):
            case _ as Token:
                return Token

                                      
"""def place_token_in_grid(g: Grid, c:Coord, t:Token) -> Optional[Grid]:

def place_token_in_row(r:Row, ca:AxisCoord, t:Token) -> Optional[Row]:
    match r:
        case(None,None,None):
            pass"""
   


def singleplayer():
    prompt_for_token()

def multiplayer():
    print("Multi Player")

def exit():
    quit()



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
    branch_to_game_feature(prompt_for_main_menu())