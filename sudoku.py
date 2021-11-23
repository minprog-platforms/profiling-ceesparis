from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):

        self._grid: dict[tuple, int] = {}
        y = 0
        x = 0
        for puzzle_row in puzzle:
            for element in puzzle_row:
                self._grid[x, y] = int(element)
                x += 1
                if x == 9:
                    x = 0
            y += 1

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[x, y] = value

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[x, y] = 0

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = self._grid[x, y]
        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

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
        values = []

        for j in range(9):
            # values.append(self.value_at(j, i))
            values.append(self._grid[j, i])

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            # values.append(self.value_at(i, j))
            values.append(self._grid[i, j])

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                # values.append(self.value_at(x, y))
                values.append(self._grid[x, y])

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        result = True

        for i in range(9):
            for value in values:
                if value not in self.column_values(i):
                    result = False
                    return result

                if value not in self.row_values(i):
                    result = False
                    return result

                if value not in self.block_values(i):
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
