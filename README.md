# sudoku-solver-py

A Sudoku solver and puzzle generator in Python. The solver uses a hybrid approach: fill cells with a single possibility first, then backtrack when needed.

## Structure

- `index.py` – Board validation, solver logic, and main entry point.
- `matrix.py` – Random Sudoku generation with configurable difficulty.

## How to run

```bash
python index.py
```

Change difficulty in `index.py`

```python
difficulty = "medium"   # Choose between: "easy", "medium", or "hard"
```

## How it works

The board is an array of 9 rows of 9 numbers (0 = empty cell). Example:

```
Solved in 0.480 seconds.
[[2,8,0,0,0,0,0,0,1],
 [0,0,0,8,0,1,0,0,4],
 [0,0,4,0,7,0,3,0,0],
 [0,2,0,0,5,0,0,6,0],
 [0,0,3,1,0,9,7,0,0],
 [0,1,0,0,8,0,0,5,0],
 [0,0,1,0,6,0,8,0,0],
 [5,0,0,2,0,3,0,0,0],
 [9,0,0,0,0,0,0,1,6]]
```

Questions @lucasinocencio1
