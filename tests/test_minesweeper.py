# tests/test_minesweeper.py

import pytest
import src.minesweeper as minesweeper

def test_module_exists():
    assert minesweeper

board_configs = [(3, 3, 2), (5, 5, 4) , (10, 10, 5)]

@pytest.mark.parametrize("rows, cols, num_mines", board_configs)
def test_place_mines(rows, cols, num_mines):
    game = minesweeper.Minesweeper(rows, cols, num_mines)
    assert (game.cols, game.rows) == (rows, cols)
    assert game.num_mines == len(game.mines) == num_mines
    assert sum(row.count("💣") for row in game.board) == game.num_mines

def test_reveal():
    # TODO : Add assertions
    pass