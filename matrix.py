import random
import copy

def generate_solved_sudoku():
    """
    Generates a complete valid solved Sudoku grid.
    """
    # Initialize a 9x9 grid with zeros
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Fill the main diagonal 3x3 blocks (easier to validate)
    fill_diagonal_blocks(grid)
    
    # Solve the rest of the Sudoku using backtracking
    solve_sudoku(grid)
    
    return grid

def fill_diagonal_blocks(grid):
    """
    Fills the diagonal 3x3 blocks with valid random numbers.
    """
    for block in range(0, 9, 3):
        fill_block(grid, block, block)

def fill_block(grid, row, col):
    """
    Fills a 3x3 block with valid random numbers.
    """
    numbers = list(range(1, 10))
    random.shuffle(numbers)
    
    for i in range(3):
        for j in range(3):
            grid[row + i][col + j] = numbers.pop()

def is_valid(grid, row, col, num):
    """
    Checks if it's valid to place 'num' at position (row, col).
    """
    # Check the row
    for x in range(9):
        if grid[row][x] == num:
            return False
    
    # Check the column
    for x in range(9):
        if grid[x][col] == num:
            return False
    
    # Check the 3x3 block
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    
    return True

def solve_sudoku(grid):
    """
    Solves the Sudoku using backtracking.
    """
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                # Try numbers from 1 to 9 in random order
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                
                for num in numbers:
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def remove_numbers(grid, difficulty):
    """
    Removes numbers from the solved grid based on difficulty level.
    
    Args:
        grid: Complete solved Sudoku grid
        difficulty: 'easy', 'medium' or 'hard'
    
    Returns:
        Partial grid with zeros in removed positions
    """
    # Create a copy of the grid
    puzzle = copy.deepcopy(grid)
    
    # Define how many numbers to remove based on difficulty
    if difficulty == 'easy':
        cells_to_remove = random.randint(30, 40)  # 30-40 numbers removed
    elif difficulty == 'medium':
        cells_to_remove = random.randint(40, 50)  # 40-50 numbers removed
    elif difficulty == 'hard':
        cells_to_remove = random.randint(50, 60)  # 50-60 numbers removed
    else:
        cells_to_remove = 40  # Default: medium
    
    # List all positions
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)
    
    # Remove numbers randomly
    removed = 0
    for row, col in positions:
        if removed >= cells_to_remove:
            break
        puzzle[row][col] = 0
        removed += 1
    
    return puzzle

def generate_random_sudoku(difficulty='medium'):
    """
    Generates a random Sudoku matrix with the specified difficulty level.
    
    Args:
        difficulty: 'easy', 'medium' or 'hard' (default: 'medium')
    
    Returns:
        2D list representing the partial Sudoku grid
    """
    # Generate a complete solved grid
    solved_grid = generate_solved_sudoku()
    
    # Remove numbers based on difficulty
    puzzle = remove_numbers(solved_grid, difficulty)
    
    return puzzle
