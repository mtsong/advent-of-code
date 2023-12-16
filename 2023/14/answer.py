import pathlib

import numpy as np

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    rows = []
    for line in f:
        rows.append(list(line.strip()))
    dish = np.array(rows)

# Tilt North
for c, column in enumerate(dish.T):
    square_rocks = []  # Indexes
    round_rocks = []  # Indexes
    for i, p in enumerate(column):
        if p == "#":
            square_rocks.append(i)
        elif p == "O":
            round_rocks.append(i)
    while round_rocks:
        square_rock = len(column)
        while square_rocks and (square_rock := square_rocks.pop(0)) > round_rocks[0]:
            pass
        if not square_rocks and square_rock > round_rocks[-1]:
            for j, round_rock in enumerate(round_rocks):
                column[round_rock] = "."
                column[j] = "O"
            break
        blocked_rounds = []
        while round_rocks and (round_rock := round_rocks[0]) >= square_rock:
            blocked_rounds.append(round_rocks.pop(0))
        if not blocked_rounds:
            blocked_rounds = round_rocks
            round_rocks = []
        for j, blocked_round in enumerate(blocked_rounds):
            column[blocked_round] = "."
            column[j] = "O"
print(dish)
print(f"The total load on the north support beams is {0}")
