import pathlib


USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    universe = []
    for line in f:
        row = []
        galaxy_in_row = False
        for char in line.strip():
            if char == "#":
                galaxy_in_row = True
            row.append(char)
        if not galaxy_in_row:
            universe.append(row)
        universe.append(row)

# Expand columns
columns = zip(*universe)
columns_with_no_galaxies = []
for i, column in enumerate(columns):
    for j, char in enumerate(column):
        if char == "#":
            break
    else:
        columns_with_no_galaxies.append(i)

for i, column in enumerate(columns_with_no_galaxies):
    for row in universe:
        row.insert(column + i, ".")

# Find galaxies
galaxies = []
for i, row in enumerate(universe):
    for j, char in enumerate(row):
        if char == "#":
            galaxies.append((i, j))

width = len(row)
height = len(universe)


total_distance = 0
distances = {}
for i, galaxy in enumerate(galaxies):
    for j, other_galaxy in enumerate(galaxies[i + 1 :]):
        total_distance += abs(galaxy[0] - other_galaxy[0]) + abs(galaxy[1] - other_galaxy[1])

print(f"The sum of the shortest path between every pair of galaxies is: {total_distance}")
