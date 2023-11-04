import numpy as np
from typing import Tuple
import logging

logger = logging.basicConfig(level=logging.INFO)
# logger = logging.basicConfig(level=logging.DEBUG)


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


# s_start = np.array(
#     [
#         [3, 0, 0, 1, 2, 8, 0, 0, 7],
#         [7, 6, 2, 3, 9, 5, 0, 8, 4],
#         [8, 1, 0, 4, 6, 7, 0, 2, 0],
#         [0, 0, 0, 2, 8, 1, 0, 0, 0],
#         [1, 0, 0, 6, 7, 3, 0, 4, 5],
#         [2, 0, 0, 9, 5, 4, 0, 0, 0],
#         [0, 2, 0, 5, 0, 9, 0, 7, 0],
#         [5, 3, 0, 7, 4, 2, 0, 9, 1],
#         [9, 0, 0, 8, 0, 6, 0, 0, 2],
#     ]
# )

s = s_start

visualize_sudoku(s)
assert s.shape[0] == 9
assert s.shape[1] == 9

n_iterations = 30

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
                # EXLUSION ALGOs (check if we can find cells where one single number is the only one that fits)
                for number in range(1, 10):
                    # ROW
                    row = s[row_idx]
                    bool_row = check_if_number_in_array(number, row)
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[row_idx, col_idx, number - 1] or bool_row
                    if bool_row:
                        logging.debug(f"Cell {row_idx} {col_idx}: {number} is in row {row}")

                    # COLUMN
                    col = s[:, col_idx]
                    bool_col = check_if_number_in_array(number, col)
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[row_idx, col_idx, number - 1] or bool_col
                    if bool_col:
                        logging.debug(f"Cell {row_idx} {col_idx}: {number} is  in col {col}")

                    # 3x3 CELL
                    cell_start_row = (row_idx // 3) * 3
                    cell_start_col = (col_idx // 3) * 3
                    cell = s[cell_start_row : cell_start_row + 3, cell_start_col : cell_start_col + 3]
                    bool_cell = check_if_number_in_array(number, cell)
                    mask_exclude[row_idx, col_idx, number - 1] = mask_exclude[row_idx, col_idx, number - 1] or bool_cell
                    if bool_cell:
                        logging.debug(f"Cell {row_idx} {col_idx}: {number} is in cell {cell.flatten()}")

                    # INSERT Numbers that can be determined by exclusion
                    logging.debug(f"Cell {row_idx} {col_idx} with number {number}: {mask_exclude[row_idx, col_idx]}")
                    if np.sum(np.logical_not(mask_exclude[row_idx, col_idx])) == 1:
                        new_val = np.where(np.logical_not(mask_exclude[row_idx, col_idx]))[0] + 1
                        s[row_idx, col_idx] = int(new_val)
                        visualize_sudoku(s, marked_cell=(row_idx, col_idx))
                        logging.info(f"Able to exclude all other number except {new_val} in {row_idx} {col_idx}")

    # COMBINATION ALGOs
    # get a (numnber, row, col) matrix instead of (row, col, number)
    mask_block = np.transpose(mask_exclude, (2, 0, 1))
    for idx in range(9):
        number = idx + 1
        logging.info(f"Check number: {number}")
        # ROW
        for row_idx in range(9):
            row = np.logical_not(mask_block[idx, row_idx])
            if np.sum(row) == 1 and number not in s[row_idx]:
                col_idx = int(np.where(row)[0])
                s[row_idx, col_idx] = number
                visualize_sudoku(s, (row_idx, col_idx))
                logging.info(f"Number {number} can only be in row {row_idx} in col {col_idx} because of row")

        for col_idx in range(9):
            col = np.logical_not(mask_block[idx, :, col_idx])
            if np.sum(col) == 1 and number not in s[:, col_idx]:
                row_idx = int(np.where(col)[0])
                s[row_idx, col_idx] = number
                visualize_sudoku(s, (row_idx, col_idx))
                logging.info(f"Number {number} can only be in row {row_idx} in col {col_idx} because of col")

        for cell_row_idx in range(3):
            for cell_col_idx in range(3):
                cell_row_start = cell_row_idx * 3
                cell_col_start = cell_col_idx * 3
                cell = np.logical_not(
                    mask_block[idx, cell_row_start : cell_row_start + 3, cell_col_start : cell_col_start + 3]
                )
                cell_values = s[cell_row_start : cell_row_start + 3, cell_col_start : cell_col_start + 3]
                if np.sum(cell.flatten()) == 1 and number not in cell_values:
                    idx_flat = int(np.where(cell.flatten())[0])
                    row_idx = idx_flat // 3
                    col_idx = idx_flat % 3
                    row_idx = cell_row_start + row_idx
                    col_idx = cell_col_start + col_idx
                    s[row_idx, col_idx] = number
                    visualize_sudoku(s, (row_idx, col_idx))
                    logging.info(
                        f"Number {number} can only be in row {row_idx} col {col_idx} in cell {cell_row_idx}, {cell_col_idx}"
                    )


print("\n------- Final Result: -------")
visualize_sudoku(s)
