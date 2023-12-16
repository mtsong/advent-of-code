import pathlib

import numpy as np

USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    rows = []
    for line in f:
        rows.append(list(line.strip()))
    dish = np.array(rows)

total_load = 0
for c, column in enumerate(dish.T):
    load = 0
    square_rocks = []  # Indexes
    round_rocks = []  # Indexes
    for i, p in enumerate(reversed(column)):
        if p == "#":
            square_rocks.append(i + 1)
        elif p == "O":
            round_rocks.append(i + 1)
    if round_rocks and not square_rocks or square_rocks and round_rocks and max(square_rocks) < min(round_rocks):
        load = (len(column) + len(column) - len(round_rocks) + 1) * len(round_rocks) // 2
        print(f"1. The load applied by column {c + 1} is {load}")
    else:
        while square_rocks and round_rocks:
            while square_rocks and (square_rock := square_rocks.pop(0)) < round_rocks[0]:
                pass
            blocked_rounds = []
            while round_rocks and (round_rock := round_rocks[0]) < square_rock:
                blocked_rounds.append(round_rocks.pop(0))
            load += (square_rock - 1 + square_rock - len(blocked_rounds)) * len(blocked_rounds) // 2
        if round_rocks:
            load += (len(column) + len(column) - len(round_rocks) + 1) * len(round_rocks) // 2
        print(f"2. The load applied by column {c + 1} is {load}")
    total_load += load
print(f"The total load on the north support beams is {total_load}")
