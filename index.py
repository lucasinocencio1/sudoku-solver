from copy import deepcopy
from pprint import pprint
import os
import time
import random
import sys
from matrix import generate_random_sudoku

SIZE = 9

def _clear_screen():
    if sys.platform.startswith("win"):
        os.system("cls")
    else:
        os.system("clear")

def _validate_grid(grid):
    """
    Validates a 9x9 Sudoku grid. Returns dict with keys:
    valid (bool), error (str or None), has_empty (bool).
    """
    flipped = [[] for _ in range(SIZE)]
    blocks = [[] for _ in range(SIZE)]
    has_empty = False

    for row, row_data in enumerate(grid):
        freq = {}
        for col, value in enumerate(row_data):
            if value == 0:
                has_empty = True
            bi = (row // 3) * 3 + (col // 3)
            blocks[bi].append(value)
            flipped[col].append(value)
            if value != 0:
                freq[value] = freq.get(value, 0) + 1
        for count in freq.values():
            if count > 1:
                return {"valid": False, "error": "duplicate_in_row", "has_empty": has_empty}

    for group in blocks:
        freq = {}
        for value in group:
            if value != 0:
                freq[value] = freq.get(value, 0) + 1
        for count in freq.values():
            if count > 1:
                return {"valid": False, "error": "duplicate_in_blocks", "has_empty": has_empty}

    for col_data in flipped:
        freq = {}
        for value in col_data:
            if value != 0:
                freq[value] = freq.get(value, 0) + 1
        for count in freq.values():
            if count > 1:
                return {"valid": False, "error": "duplicate_in_col", "has_empty": has_empty}

    return {"valid": True, "error": None, "has_empty": has_empty}


class Board:
    def __init__(self, board):
        self.board = deepcopy(board)
        self.backup = deepcopy(board)
        self.last_choice = 0

    def get_board(self):
        """
        Get the current board.
        """
        return self.board

    def set_backup(self, board):
        """
        Set the backup board.
        """
        self.backup = deepcopy(board)

    def restore_backup(self):
        """
        Restore the backup board.
        """
        self.board = deepcopy(self.backup)

    def is_solved(self):
        """
        Check if the board is solved.
        """
        r = _validate_grid(self.board)
        if not r["valid"]:
            return {"solved": False, "error": r["error"]}
        if r["has_empty"]:
            return {"solved": False, "error": "empty_space"}
        return {"solved": True}

    def has_errors(self, grid):
        """
        Check if the board has errors.
        """
        r = _validate_grid(grid)
        return {"errors": not r["valid"], "error": r["error"]}

    def place_number(self, row, col, value):  
        """
        Place a number on the board.
        """
        new_board = deepcopy(self.board)
        new_board[row] = deepcopy(self.board[row])
        new_board[row][col] = value
        if self.has_errors(new_board)["errors"]:
            return {"errors": True, "error": "illegal_placement"}
        self.board = new_board
        return {"errors": False, "board": new_board}

    def can_place(self, row, col, value): 
        """
        Check if a number can be placed on the board.
        """
        new_board = deepcopy(self.board)
        new_board[row] = deepcopy(self.board[row])
        new_board[row][col] = value
        return self.has_errors(new_board)

    def get_cell(self, row, col):
        """
        Get a cell from the board.
        """
        return self.board[row][col]


def _build_possibilities(board):
    """Build a 9x9 structure: each cell is either the fixed digit or a list of possible digits."""
    possibilities = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            v = board.get_cell(r, c)
            if v != 0:
                row.append(v)
            else:
                row.append([n for n in range(1, 10) if not board.can_place(r, c, n)["errors"]])
        possibilities.append(row)
    return possibilities


def _fill_singles_and_recurse(sudoku, step, start_time, on_progress):
    """
    Fill cells with a single possibility; otherwise branch with backtracking.
    step: -1 = first call (set backup), 0 = normal, 1 = backtrack retry.
    Returns solved board or None if impossible.
    """
    possibilities = _build_possibilities(sudoku)
    has_singular = False
    invalid = False

    for row in range(SIZE):
        for col in range(SIZE):
            cell = possibilities[row][col]
            if isinstance(cell, list):
                if len(cell) == 0:
                    invalid = True
                elif len(cell) == 1:
                    has_singular = True
                    sudoku.place_number(row, col, cell[0])
                    if step == -1:
                        sudoku.set_backup(sudoku.get_board())
                    if on_progress:
                        on_progress(sudoku.get_board())
                    return _fill_singles_and_recurse(sudoku, 0, start_time, on_progress)

    if invalid:
        sudoku.restore_backup()
        if step == -1:
            return None
        return _fill_singles_and_recurse(sudoku, -1, start_time, on_progress)

    if has_singular:
        return _fill_singles_and_recurse(sudoku, 0, start_time, on_progress)

    if sudoku.is_solved()["solved"]:
        return sudoku.get_board()

    if step == 1:
        sudoku.restore_backup()
        return _fill_singles_and_recurse(sudoku, 1, start_time, on_progress)

    sudoku.set_backup(sudoku.get_board())
    for row in range(SIZE):
        for col in range(SIZE):
            cell = possibilities[row][col]
            if isinstance(cell, list) and len(cell) > 0:
                choices = [x for x in cell if x != sudoku.last_choice]
                if not choices:
                    choices = cell
                choice = random.choice(choices)
                sudoku.last_choice = choice
                sudoku.place_number(row, col, choice)
                result = _fill_singles_and_recurse(sudoku, 0, start_time, on_progress)
                if result is not None:
                    return result
                sudoku.restore_backup()
    return None


def solve(sudoku, on_progress=None):
    """
    Solve the Sudoku. Returns solved board (list of lists) or None if impossible.
    on_progress: optional callback(board) called when the board updates (e.g. for display).
    """
    return _fill_singles_and_recurse(sudoku, -1, time.perf_counter(), on_progress)


# Main function

# Difficulty: "easy" (fewer blanks), "medium", "hard"
difficulty = "medium"
puzzle = generate_random_sudoku(difficulty)
sudoku = Board(puzzle)

_clear_screen()
print(f"Difficulty: {difficulty}")
print("Initial board:")
pprint(sudoku.get_board())

def show(board):
    _clear_screen()
    pprint(board)

start = time.perf_counter()
result = solve(sudoku, on_progress=show)
elapsed = time.perf_counter() - start

if result is None:
    print("Impossible to solve.")
else:
    _clear_screen()
    print(f"Solved in {elapsed:.3f} seconds.")
    pprint(result)
