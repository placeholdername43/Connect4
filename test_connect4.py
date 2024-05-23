import pytest
import sys
from connect4 import *

def test_parse_main_menu_singleplayer_valid():
    assert all(map(lambda input_p: MainMenuOption.parse(input_p) == MainMenuOption.SinglePlayer, ["singleplayer", "1"]))     
  
def test_parse_main_menu_multiplayer_valid():
    assert all(map(lambda input_p: MainMenuOption.parse(input_p) == MainMenuOption.MultiPlayer, ["multiplayer", "2"]))     

def test_parse_main_menu_exit_valid():
    assert all(map(lambda input_p: MainMenuOption.parse(input_p) == MainMenuOption.Exit, ["exit", "3"]))     

def test_parse_main_menu_invalid():
    assert all(map(lambda input_p: MainMenuOption.parse(input_p) == None, ["aaaa", "3000"]))       
  
def test_parse_exit_yes():
    assert parse_exit("Y") == True

def test_parse_exit_no():
    assert parse_exit("N") == False

def test_parse_token_valid_Red():
    assert all(map(lambda input_p: isinstance(parse_token(input_p), R), ["r", "1", "red"]))       

def test_parse_token_valid_Yellow():
    assert all(map(lambda input_p: isinstance(parse_token(input_p), Y), ["y", "2", "yellow"]))  

def test_parse_token_invalid_input():
    assert all(map(lambda input_p: (parse_token(input_p) == None), ["g","900","green"]))           

def test_parse_column_valid():
    assert parse_column("1") == 0
    assert parse_column("7") == 6

def test_parse_column_invalid():
    assert all(map(lambda input_p: (parse_column(input_p) == None), ["-5","900","column 5043"]))         

def test_exit_game(monkeypatch):
    monkeypatch.setattr('connect4.prompt_for_exit_confirmation', lambda: True)
    with pytest.raises(SystemExit) as sys_exit:
        exit_game()
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0

def test_not_exit_game(monkeypatch):
    monkeypatch.setattr('connect4.prompt_for_exit_confirmation', lambda: False)
    
def test_drop_token_in_empty_column():
    column = (None, None, None, None, None, None)
    new_column = drop_token_in_column(column, R())
    assert new_column == (R(), None, None, None, None, None)

def test_drop_token_in_full_column():
    full_column = (R(), R(), R(), R(), R(), R())
    assert drop_token_in_column(full_column, R()) is None

def test_check_for_win_horizontal():
    grid = create_empty_grid()
    grid = place_new_column_in_grid(grid, 0, (R(), None, None, None, None, None))
    grid = place_new_column_in_grid(grid, 1, (R(), None, None, None, None, None))
    grid = place_new_column_in_grid(grid, 2, (R(), None, None, None, None, None))
    grid = place_new_column_in_grid(grid, 3, (R(), None, None, None, None, None))
    assert check_for_win(grid, R())

def test_check_for_win_vertical():
    grid = create_empty_grid()
    grid = place_new_column_in_grid(grid, 0, (R(), R(), R(), R(), None, None))
    assert check_for_win(grid, R())

def test_check_for_win_diagonal():
    grid = create_empty_grid()
    grid = place_new_column_in_grid(grid, 0, (R(), None, None, None, None, None))
    grid = place_new_column_in_grid(grid, 1, (None, R(), None, None, None, None))
    grid = place_new_column_in_grid(grid, 2, (None, None, R(), None, None, None))
    grid = place_new_column_in_grid(grid, 3, (None, None, None, R(), None, None))
    assert check_for_win(grid, R())

if __name__ == "__main__":
    pytest.main()
