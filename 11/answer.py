import pathlib


USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    universe = []
    rows_with_no_galaxies = set()
    for i, line in enumerate(f):
        row = []
        galaxy_in_row = False
        for char in line.strip():
            if char == "#":
                galaxy_in_row = True
            row.append(char)
        if not galaxy_in_row:
            rows_with_no_galaxies.add(i)
        universe.append(row)

# Find columns with no galaxies
columns = zip(*universe)
columns_with_no_galaxies = set()
for i, column in enumerate(columns):
    for j, char in enumerate(column):
        if char == "#":
            break
    else:
        columns_with_no_galaxies.add(i)

# Find galaxies
galaxies = []
for i, row in enumerate(universe):
    for j, char in enumerate(row):
        if char == "#":
            galaxies.append((i, j))

width = len(row)
height = len(universe)

space_expansion_factor = 1000000
total_distance = 0
distances = {}
for i, galaxy in enumerate(galaxies):
    for j, other_galaxy in enumerate(galaxies[i + 1 :]):
        distance = abs(galaxy[0] - other_galaxy[0]) + abs(galaxy[1] - other_galaxy[1])
        # Find crosses of expanded rows/columns
        x_range = range(min(galaxy[1], other_galaxy[1]), max(galaxy[1], other_galaxy[1]) + 1)
        y_range = range(min(galaxy[0], other_galaxy[0]), max(galaxy[0], other_galaxy[0]) + 1)
        for column in columns_with_no_galaxies:
            if column in x_range:
                distance += space_expansion_factor - 1
        for row in rows_with_no_galaxies:
            if row in y_range:
                distance += space_expansion_factor - 1
        total_distance += distance

print(f"The sum of the shortest path between every pair of galaxies is: {total_distance}")
