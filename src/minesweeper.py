"""This module implements the Minesweeper game."""

from __future__ import annotations

import random


class Minesweeper:
    def __init__(self, rows: int, cols: int, num_mines: int) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be greater than 0")

        if num_mines < 0 or num_mines >= rows * cols:
            raise ValueError("num_mines must be between 0 and rows * cols - 1")

        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines

        self.board: list[list[int | str]] = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mines: set[tuple[int, int]] = set()
        self.revealed: set[tuple[int, int]] = set()
        self.flagged: set[tuple[int, int]] = set()
        self.game_over = False

        self.place_mines()

    def place_mines(self) -> None:
        """Place mines and compute adjacent mine counts."""
        while len(self.mines) < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            if (row, col) in self.mines:
                continue

            self.mines.add((row, col))
            self.board[row][col] = "💣"

        for row, col in self.mines:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if not self.is_in_bounds(i, j):
                        continue

                    if self.board[i][j] == "💣":
                        continue

                    self.board[i][j] += 1

    def is_in_bounds(self, row: int, col: int) -> bool:
        """Check whether a cell is inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def toggle_flag(self, row: int, col: int) -> str:
        """Mark or unmark a cell with a flag."""
        if self.game_over:
            return "Game Over"

        if not self.is_in_bounds(row, col):
            return "Invalid Cell"

        if (row, col) in self.revealed:
            return "Already Revealed"

        if (row, col) in self.flagged:
            self.flagged.remove((row, col))
            return "Unflagged"

        self.flagged.add((row, col))
        return "Flagged"

    def reveal(self, row: int, col: int) -> str:
        """Reveal a cell."""
        if self.game_over:
            return "Game Over"

        if not self.is_in_bounds(row, col):
            return "Invalid Cell"

        if (row, col) in self.flagged:
            return "Flagged"

        if (row, col) in self.revealed:
            return "Already Revealed"

        if (row, col) in self.mines:
            self.game_over = True
            return "Game Over"

        self._flood_fill(row, col)
        return "Continue"

    def _flood_fill(self, row: int, col: int) -> None:
        """Reveal adjacent empty cells recursively."""
        if not self.is_in_bounds(row, col):
            return

        if (row, col) in self.revealed:
            return

        if (row, col) in self.flagged:
            return

        if (row, col) in self.mines:
            return

        self.revealed.add((row, col))

        if self.board[row][col] != 0:
            return

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i, j) != (row, col):
                    self._flood_fill(i, j)

    def get_board(self) -> list[list[str | int]]:
        """Return the visible board for the player."""
        visible_board: list[list[str | int]] = []

        for row in range(self.rows):
            visible_row: list[str | int] = []

            for col in range(self.cols):
                if (row, col) in self.flagged:
                    visible_row.append("🚩")
                elif (row, col) not in self.revealed:
                    visible_row.append(" ")
                else:
                    cell = self.board[row][col]
                    visible_row.append("0" if cell == 0 else cell)

            visible_board.append(visible_row)

        return visible_board

    def get_full_board(self) -> list[list[str | int]]:
        """Return the full board, revealing mines and values."""
        full_board: list[list[str | int]] = []

        for row in range(self.rows):
            full_row: list[str | int] = []

            for col in range(self.cols):
                if (row, col) in self.mines:
                    full_row.append("💣")
                elif (row, col) in self.flagged and (row, col) not in self.mines:
                    full_row.append("❌")
                else:
                    cell = self.board[row][col]
                    full_row.append("0" if cell == 0 else cell)

            full_board.append(full_row)

        return full_board

    def is_winner(self) -> bool:
        """Check if the player has won."""
        return len(self.revealed) == (self.rows * self.cols - self.num_mines)

    def restart(self) -> None:
        """Restart the game with the same parameters."""
        self.__init__(self.rows, self.cols, self.num_mines)