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
for i, mirror in enumerate(mirrors):
    print(f"Finding symmetrical rows and columns for mirror {i + 1}")
    # Check columns
    vertical_line_found = False
    identical_columns = []
    for i in range(len(mirror[0])):
        for j in range(i + 1, len(mirror[0])):
            if np.array_equal(mirror[:, i], mirror[:, j]):
                identical_columns += [i, j]
    if sum(np.diff(sorted(identical_columns)) == 1) >= len(identical_columns) - 1:
        left = len(identical_columns) // 2
        print(f"Columns {left + 1} and {left + 2} form the vertical line of symmetry")
        total += left + 1
        vertical_line_found = True
    # Check rows
    if not vertical_line_found:
        identical_rows = []
        for i in range(len(mirror)):
            for j in range(i + 1, len(mirror)):
                if np.array_equal(mirror[i], mirror[j]):
                    identical_rows += [i, j]
        if sum(np.diff(sorted(identical_rows)) == 1) >= len(identical_rows) - 1:
            top = len(identical_rows) // 2
            print(f"Rows {top + 1} and {top + 2} form the horizontal line of symmetry")
            total += (top + 1) * 100
print(f"The number after summarizing all of my notes is {total}")
