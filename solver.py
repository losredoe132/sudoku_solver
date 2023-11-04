import numpy as np
from typing import Tuple
import logging

logger = logging.basicConfig(level=logging.DEBUG)


def visualize_sudoku(s, marked_cell=None):
    print("-" * 36)

    for row_idx, row in enumerate(s):
        if row_idx % 3 == 0 and row_idx > 0:
            print("-" * 36)
        for col_idx, val in enumerate(row):
            if col_idx % 3 == 0 and col_idx > 0:
                print(" | ", end="")
            if marked_cell is not None and row_idx == marked_cell[0] and col_idx == marked_cell[1]:
                print(f"({val})" if val != 0 else "   ", end="")
            else:
                print(f" {val} " if val != 0 else "   ", end="")

        print()
    print("-" * 36)
    print()
    print()


def check_if_number_in_array(number: int, array: np.ndarray):
    return number in list(array.flatten())


s_start = np.array(
    [
        [3, 0, 0, 1, 0, 8, 0, 0, 7],
        [7, 6, 0, 0, 9, 0, 0, 8, 4],
        [0, 1, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 2, 8, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 9, 5, 4, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 7, 0],
        [5, 3, 0, 0, 4, 0, 0, 9, 1],
        [9, 0, 0, 8, 0, 6, 0, 0, 2],
    ]
)
s = s_start

visualize_sudoku(s)
assert s.shape[0] == 9
assert s.shape[1] == 9

n_iterations = 3

# create exclusion mask
mask_exclude = np.zeros((9, 9, 9))

for i in range(n_iterations):
    # check rows
    for row_idx in range(9):
        for col_idx in range(9):
            if s[row_idx, col_idx] > 0:
                # ALREADY DEFINED
                number = s[row_idx, col_idx]
                mask = np.ones(9)
                mask[number - 1] = 0
                mask_exclude[row_idx, col_idx, :] = mask
                logging.debug(f"Cell {row_idx} {col_idx}: {number} is already defined.")
            else:
                for number in range(1, 10):
                    # ROW
                    row = s[row_idx]
                    b = check_if_number_in_array(number, row)
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[row_idx, col_idx, number - 1] or b
                    logging.debug(f"Cell {row_idx} {col_idx}: {number} is {'   ' if b else 'not'} in row {row}")

                    # COLUMN
                    col = s[:, col_idx]
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[
                        row_idx, col_idx, number - 1
                    ] or check_if_number_in_array(number, col)
                    logging.debug(f"Cell {row_idx} {col_idx}: {number} is {'' if b else 'not'} in col {col}")

                    # 3x3 CELL
                    cell_start_row = row_idx // 3
                    cell_start_col = col_idx // 3
                    cell = s[cell_start_row : cell_start_row + 3, cell_start_col : cell_start_col + 3]
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[
                        row_idx, col_idx, number - 1
                    ] or check_if_number_in_array(number, cell)
                    logging.debug(f"Cell {row_idx} {col_idx}: {number} is {'' if b else 'not'} in cell {cell}")

    # check if there is a single cell with only one true
    for row_idx in range(9):
        for col_idx in range(9):
            if np.sum(np.logical_not(mask_exclude[row_idx, col_idx])) == 1:
                s[row_idx, col_idx] = np.where(np.logical_not(mask_exclude[row_idx, col_idx]))[0] + 1
                visualize_sudoku(s, marked_cell=(row_idx, col_idx))
