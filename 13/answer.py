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
    # Check columns
    vertical_line_found = False
    lefts = []
    rights = []
    identical_columns = []
    leftest = len(mirror[0])
    rightest = 0
    for i in range(len(mirror[0])):
        for j in range(i + 1, len(mirror[0])):
            if np.array_equal(mirror[:, i], mirror[:, j]):
                if i < leftest:
                    leftest = i
                if j > rightest:
                    rightest = j
                identical_columns.append((i + 1, j + 1))
                lefts.append(i + 1)
                rights.append(j + 1)
    if identical_columns:
        if lefts[0] == 1:
            prev_left, prev_right = lefts[0], rights[0]
            column_sum = prev_left + prev_right
            for left, right in zip(lefts[1:], rights[1:]):
                if left == prev_left + 1 and right == prev_right - 1 and left + right == column_sum:
                    prev_left, prev_right = left, right
                else:
                    break
            if right == left + 1:
                print(f"Columns {left} and {right} form the vertical line of symmetry for mirror {mirror_num + 1}")
                total += left
                vertical_line_found = True
        if not vertical_line_found and rights[-1] == len(mirror[0]):
            prev_left, prev_right = lefts[-1], rights[-1]
            column_sum = prev_left + prev_right
            for left, right in zip(reversed(lefts)[:-1], reversed(rights[:-1])):
                if left == prev_left + 1 and right == prev_right - 1 and left + right == column_sum:
                    prev_left, prev_right = left, right
                else:
                    break
            print(f"Columns {left} and {right} form the vertical line of symmetry for mirror {mirror_num + 1}")
            total += left
            vertical_line_found = True
    # Check rows
    if not vertical_line_found:
        identical_rows = []
        for i in range(len(mirror)):
            for j in range(i + 1, len(mirror)):
                if np.array_equal(mirror[i], mirror[j]):
                    identical_rows.append((i + 1, j + 1))
        top, bottom = identical_rows[-1]
        print(f"Rows {top} and {top + 1} form the horizontal line of symmetry for mirror {mirror_num + 1}")
        total += top * 100
print(f"The number after summarizing all of my notes is {total}")
