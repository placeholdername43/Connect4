from enum import Enum
from typing import TypeAlias, Optional, List
import sys
import random

def compose(f, g):
    return lambda x: f(g(x))

increment = lambda x: x+1
square = lambda x: x*x
double_it = lambda x: x+x



"""
This can be any string that is typed in via the keyboard
"""
InputText: TypeAlias = str

"""
MainMenu
let mainMenu = { (RollSingle, 1), (RollMultiple, 2), (Exit, 3) }
"""

class MenuOption(Enum):
    RollSingle = 1
    RollMultiple = 2
    Exit = 3
    @staticmethod
    def parse(s: InputText) -> Optional['MenuOption']: # This is a forward declaration, as the identifier has not been given a complete declaration  yet
        # it means come back when you do figure it out and are able to give valid return values 
        match s.strip().lower():
            case "1" | "single": return MenuOption.RollSingle
            case "2" | "many": return MenuOption.RollMultiple
            case "3" | "exit": return MenuOption.Exit
            case _: return None

# enums r used when ur tryna match a value to a type 
class Dice(Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20

    @staticmethod
    def parse(s: InputText) -> Optional['Dice']:
        match s.strip().lower(): # canonicalising our input
            case "d4" | "4": return Dice.D4
            case "d6" | "6": return Dice.D4
            case "d8" | "8": return Dice.D4
            case "d10" | "10": return Dice.D4
            case "d12" | "12": return Dice.D4
            case "d20" | "20": return Dice.D4
            case _: return None
    
    @staticmethod
    def roll(d:Optional['Dice']) -> int :
        return random.choice(range(1, d.value + 1))

"""
DicePool
A collection of dice of the same type
With a tuple: need to know how many dice are required
Sequences allow us to take an index value and relate it to a particular dice type
"""
DicePool: TypeAlias = List[Dice]
def print_dice_pool(dp: List[int]):
    for idx, r in enumerate(dp):
        print("Roll was: {0} was {1}".format(idx+1, r))

"""
DiceAmount
Min: 1
Max: 10

let DiceAmount = {1,2,3,4,5,6,7,8,9,10}
DiceAmount will be a subset of int
"""
class DiceAmount(int):
    def __new__(cls, count):
        if 0 < count <= 10:
            return super(DiceAmount, cls).__new__(cls, count)
        else:
            raise ValueError("DiceAmount must be between 1 and 10")
    @staticmethod
    def parse(s: InputText) -> Optional['DiceAmount']:
        try:
            return DiceAmount(int(s))
        except ValueError:
            return None
        
"""
Dice Choice prompt
1. Read dice choice input
2. read dice choice input
3. if dicechoice valid
    return dicechoice in valid format
    otherwise
    output an error message to the standard error
  else goto 1

""" 

def prompt_for_input(parse_func, message, err_msg):
    def inner():
        while True:
            match parse_func(input(message)):
                case None:
                    print(err_msg, file=sys.stderr)
                case x:
                    return x
    return inner

prompt_for_dice_choice = prompt_for_input(Dice.parse, 
                                          "Enter a dice choice (e.g d4): ", 
                                          "ERROR: Invalid dice choice")

prompt_for_dice_amount = prompt_for_input(DiceAmount.parse, 
                                          "please input a valid dice amount (1-10): ", 
                                          "ERROR: Invalid dice choice")

prompt_for_menu_option = prompt_for_input(MenuOption.parse, 
                                          "Please choose an option\n (1 - roll 1 dice \n 2 - multiple dice \n 3 - exit): ", 
                                          "ERROR: Invalid menu option")

def roll_single() -> int:
    """
    prompt for dice choice
    roll dice choice
    print the result
    return exit code indicating success
    """
    print(Dice.roll(prompt_for_dice_choice()), file = sys.stdout)
    return 0

def roll_many() -> int:
    """ prompt for the dice amount
    for the amount chosen:
        prompt for the dice choice
        roll the dice pool
        print the result
        return exit code indicating success
        """
    
    """
    amt:DiceAmount = prompt_for_dice_amount()
    dice_pool = list(map(lambda x: prompt_for_dice_choice() , range(0, amt)))  # simulate that a value is passed in cuz we dont have a value to pass in
    roll_result : int = -1
    print(roll_result)
    return 0
    """

    amt:DiceAmount = prompt_for_dice_amount()
    dice_pool = (prompt_for_dice_choice() for i in range(0,amt))  # simulate that a value is passed in cuz we dont have a value to pass in
    roll_result : int = list(map(Dice.roll, dice_pool))#  gives python the opportunity to combine the two functions in one
    print(roll_result)
    print_dice_pool(roll_result)
    return 0

def exit_program() -> int:
    print("Now exiting the dice roller program")
    sys.exit(0)

def main(argv:List[str]) -> int:
    """
    prompt for menu options
    then branch to feature and from that feature
    """

    menu_choice : MenuOption = prompt_for_menu_option()
    match menu_choice:
        case MenuOption.RollSingle:
            return roll_single()
        case MenuOption.RollMultiple:
            return roll_many()


if __name__ == "__main__":
    sys.exit(main(sys.argv))