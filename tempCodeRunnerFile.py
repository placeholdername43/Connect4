import pytest
import sys

# Assuming the classes and functions are defined in a module named `connect_four`
from connect4 import MainMenuOption, parse_token, parse_column, drop_token_in_column, check_for_win, create_empty_grid, place_new_column_in_grid, R, Y

def test_parse_main_menu():
    assert MainMenuOption.parse("1") == MainMenuOption.SinglePlayer
    assert MainMenuOption.parse("2") == MainMenuOption.MultiPlayer
    assert MainMenuOption.parse("3") == MainMenuOption.Exit
    assert MainMenuOption.parse("4") is None  # Invalid option

def test_parse_token():
    assert isinstance(parse_token("R"), R)
    assert isinstance(parse_token("1"), R)
    assert isinstance(parse_token("y"), Y)
    assert isinstance(parse_token("2"), Y)
    assert parse_token("green") is None  # Invalid token

def test_parse_column():
    assert parse_column("1") == 0
    assert parse_column("7") == 6
    assert parse_column("8") is None  # Out of bounds
    assert parse_column("zero") is None  # Non-numeric

def test_drop_token_in_column():
    column = (None, None, None, None, None, None)
    new_column = drop_token_in_column(column, R())
    assert new_column == (R(), None, None, None, None, None)

    full_column = (R(), R(), R(), R(), R(), R())
    assert drop_token_in_column(full_column, R()) is None  # Column is full

def test_check_for_win_horizontal():
    grid = create_empty_grid()
    grid = place_new_column_in_grid(grid, 0, (R(), R(), R(), None, None, None))
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

