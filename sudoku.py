from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):

        self._grid: dict[tuple, int] = {}
        self.row_list: list[list: int] = []
        self.column_list: list[list: int] = []
        self.block_list: list[list: int] = []
        y = 0
        x = 0
        for puzzle_row in puzzle:
            sing_row = []
            for element in puzzle_row:
                val_sq = int(element)
                self._grid[x, y] = val_sq
                sing_row.append(val_sq)
                x += 1
                if x == 9:
                    x = 0
            self.row_list.append(sing_row)
            y += 1
        for i in range(9):
            sing_col = []
            for j in range(9):
                val_col = self._grid[i, j]
                sing_col.append(val_col)
            self.column_list.append(sing_col)

        block_row_list = []
        for i in range(9):
            x_start = (i % 3) * 3
            y_start = (i // 3) * 3

            for y in range(y_start, y_start + 3):
                sing_block_row = []
                for x in range(x_start, x_start + 3):
                    sing_block_row.append(self._grid[x, y])
                block_row_list.append(sing_block_row)

        for i in range(0, 27, 3):
            whole_block = block_row_list[i] + block_row_list[i+1] + block_row_list[i+2]
            self.block_list.append(whole_block)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[x, y] = value
        self.row_list[y][x] = value
        self.column_list[x][y] = value
        block_num = (y // 3) * 3 + x // 3
        rel_block = self.block_list[block_num]
        index_num = (y % 3) * 3 + x % 3
        rel_block[index_num] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[x, y] = 0
        self.row_list[y][x] = 0
        self.column_list[x][y] = 0
        block_num = (y // 3) * 3 + x // 3
        rel_block = self.block_list[block_num]
        index_number = (y % 3) * 3 + x % 3
        rel_block[index_number] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = self._grid[x, y]
        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

        values_row = set(self.row_values(y))
        options = options - values_row
        columns_row = set(self.column_values(x))
        options = options - columns_row

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        block_row = set(self.block_values(block_index))
        options = options - block_row

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self._grid[x, y] == 0:
                    return x, y
        x, y = -1, -1
        return x, y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""

        values = self.row_list[i]
        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""

        values = self.column_list[i]
        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """

        values = self.block_list[i]
        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """

        zero = 0
        result = True

        for i in range(9):
            if zero in self.column_values(i):
                result = False
                return result

            if zero in self.row_values(i):
                result = False
                return result

            if zero in self.row_values(i):
                result = False
                return result

        return result

    def __str__(self) -> str:
        representation = ""

        for y in range(9):
            for x in range(9):
                representation += str(self._grid[x, y])
            representation += "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
