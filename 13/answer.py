import pathlib

import numpy as np

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    mirrors = []
    mirror = []
    for line in f:
        if line.strip() == "":
            mirrors.append(np.array(mirror))
            mirror = []
        else:
            mirror.append(list(line.strip()))
    mirrors.append(np.array(mirror))

total = 0
for mirror_num, mirror in enumerate(mirrors):
    # Vertical flip from start
    column = 0
    found = False
    left = 0
    while not found and column < len(mirror[0]) - 1:
        submirror = mirror[:, column:]
        flipped = np.flip(submirror, axis=1)
        if np.array_equal(submirror, flipped):
            lor = (left + len(mirror[0])) // 2
            print(f"Column {lor} and {lor + 1} form the vertical line of symmetry for mirror {mirror_num + 1}")
            total += lor
            found = True
        else:
            column += 1
            left += 1
    # Vertical flip from end
    if not found:
        column = len(mirror[0]) - 1
        right = column
        while not found and column > 1:
            submirror = mirror[:, :column]
            flipped = np.flip(submirror, axis=1)
            if np.array_equal(submirror, flipped):
                lor = (right + len(mirror[0])) // 2
                print(f"Column {lor} and {lor + 1} form the vertical line of symmetry for mirror {mirror_num + 1}")
                total += lor
                found = True
            else:
                column -= 1
    # Horizontal flip from top
    if not found:
        row = 0
        while not found and row < len(mirror):
            submirror = mirror[row:, :]
            flipped = np.flip(submirror, axis=0)
            if np.array_equal(submirror, flipped):
                lor = len(mirror) // 2 + 1
                print(f"Row {lor} and {lor + 1} form the horizontal line of symmetry for mirror {mirror_num + 1}")
                total += lor * 100
                found = True
            else:
                row += 1
    # Horizontal flip from bottom
    if not found:
        row = len(mirror) - 1
        while not found and row > 1:
            submirror = mirror[:row, :]
            flipped = np.flip(submirror, axis=0)
            if np.array_equal(submirror, flipped):
                lor = len(mirror) // 2 + 1
                print(f"Row {lor} and {lor + 1} form the horizontal line of symmetry for mirror {mirror_num + 1}")
                total += lor * 100
                found = True
            else:
                row -= 1
    # # Check columns
    # vertical_line_found = False
    # lefts = []
    # rights = []
    # identical_columns = []
    # for i in range(len(mirror[0])):
    #     for j in range(i + 1, len(mirror[0])):
    #         if np.array_equal(mirror[:, i], mirror[:, j]):
    #             identical_columns.append((i + 1, j + 1))
    #             lefts.append(i + 1)
    #             rights.append(j + 1)
    # if identical_columns:
    #     if len(identical_columns) == 1:
    #         print(
    #             f"Columns {identical_columns[0][0]} and {identical_columns[0][1]} form the vertical line of symmetry for mirror {mirror_num + 1}"
    #         )
    #         total += identical_columns[0][0]
    #         vertical_line_found = True
    #     else:
    #         if min(lefts) == 1:
    #             prev_left, prev_right = lefts[0], rights[0]
    #             column_sum = prev_left + prev_right
    #             run_length = 1
    #             for left, right in zip(lefts[1:], rights[1:]):
    #                 if left == prev_left + 1 and right == prev_right - 1 and left + right == column_sum:
    #                     prev_left, prev_right = left, right
    #                     run_length += 1
    #                 elif left == prev_left or right == prev_right or left == prev_left + 1 or right == prev_right - 1:
    #                     prev_left, prev_right = left, right
    #                 elif run_length > 1:
    #                     break
    #                 else:
    #                     column_sum = left + right
    #             if right == left + 1:
    #                 print(f"Columns {left} and {right} form the vertical line of symmetry for mirror {mirror_num + 1}")
    #                 total += left
    #                 vertical_line_found = True
    #             elif prev_right == prev_left + 1:
    #                 print(
    #                     f"Columns {prev_left} and {prev_right} form the vertical line of symmetry for mirror {mirror_num + 1}"
    #                 )
    #                 total += prev_left
    #                 vertical_line_found = True
    #         if not vertical_line_found and max(rights) == len(mirror[0]):
    #             prev_left, prev_right = lefts[-1], rights[-1]
    #             column_sum = prev_left + prev_right
    #             run_length = 1
    #             run_start = None
    #             for left, right in zip(list(reversed(lefts))[1:], list(reversed(rights))[1:]):
    #                 if left == prev_left - 1 and right == prev_right + 1 and left + right == column_sum:
    #                     if run_start is None:
    #                         run_start = (prev_left, prev_right)
    #                     prev_left, prev_right = left, right
    #                     run_length += 1
    #                 elif left == prev_left or right == prev_right or left == prev_left - 1 or right == prev_right + 1:
    #                     prev_left, prev_right = left, right
    #                 elif run_length > 1:
    #                     break
    #                 else:
    #                     column_sum = left + right
    #             if right == left + 1:
    #                 print(f"Columns {left} and {right} form the vertical line of symmetry for mirror {mirror_num + 1}")
    #                 total += left
    #                 vertical_line_found = True
    #             elif prev_right == prev_left + 1:
    #                 print(
    #                     f"Columns {prev_left} and {prev_right} form the vertical line of symmetry for mirror {mirror_num + 1}"
    #                 )
    #                 total += prev_left
    #                 vertical_line_found = True
    # # Check rows
    # if not vertical_line_found:
    #     tops = []
    #     bottoms = []
    #     identical_rows = []
    #     for i in range(len(mirror)):
    #         for j in range(i + 1, len(mirror)):
    #             if np.array_equal(mirror[i], mirror[j]):
    #                 identical_rows.append((i + 1, j + 1))
    #                 tops.append(i + 1)
    #                 bottoms.append(j + 1)
    #     if len(identical_rows) == 1:
    #         print(
    #             f"Rows {identical_rows[0][0]} and {identical_rows[0][1]} form the horizontal line of symmetry for mirror {mirror_num + 1}"
    #         )
    #         total += identical_rows[0][0] * 100
    #     else:
    #         found = False
    #         if min(tops) == 1:
    #             prev_top, prev_bottom = tops[0], bottoms[0]
    #             row_sum = prev_top + prev_bottom
    #             run_length = 1
    #             for top, bottom in zip(tops[1:], bottoms[1:]):
    #                 if top == prev_top + 1 and bottom == prev_bottom - 1 and top + bottom == row_sum:
    #                     prev_top, prev_bottom = top, bottom
    #                     run_length += 1
    #                 elif top == prev_top or bottom == prev_bottom or top == prev_top + 1 or bottom == prev_bottom - 1:
    #                     prev_top, prev_bottom = top, bottom
    #                 elif run_length > 1:
    #                     break
    #                 else:
    #                     row_sum = top + bottom
    #             if bottom == top + 1:
    #                 print(f"Rows {top} and {bottom} form the horizontal line of symmetry for mirror {mirror_num + 1}")
    #                 total += top * 100
    #                 found = True
    #             elif prev_bottom == prev_top + 1:
    #                 print(
    #                     f"Rows {prev_top} and {prev_bottom} form the horizontal line of symmetry for mirror {mirror_num + 1}"
    #                 )
    #                 total += prev_top * 100
    #                 found = True
    #         if not found:
    #             prev_top, prev_bottom = tops[-1], bottoms[-1]
    #             row_sum = prev_top + prev_bottom
    #             run_length = 1
    #             for top, bottom in zip(list(reversed(tops))[1:], list(reversed(bottoms))[1:]):
    #                 if top == prev_top - 1 and bottom == prev_bottom + 1 and top + bottom == row_sum:
    #                     prev_top, prev_bottom = top, bottom
    #                     run_length += 1
    #                 elif top == prev_top or bottom == prev_bottom or top == prev_top - 1 or bottom == prev_bottom + 1:
    #                     prev_top, prev_bottom = top, bottom
    #                 elif run_length > 1:
    #                     break
    #                 else:
    #                     row_sum = top + bottom
    #             if bottom == top + 1:
    #                 print(f"Rows {top} and {bottom} form the horizontal line of symmetry for mirror {mirror_num + 1}")
    #                 total += top * 100
    #             else:
    #                 print(
    #                     f"Rows {prev_top} and {prev_bottom} form the horizontal line of symmetry for mirror {mirror_num + 1}"
    #                 )
    #                 total += prev_top * 100
print(f"The number after summarizing all of my notes is {total}")
