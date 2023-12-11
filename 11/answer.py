import pathlib
import queue


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


def bfs(start: tuple[int, int], end: tuple[int, int]) -> int:
    q = queue.SimpleQueue()
    q.put([(start[1], start[0])])
    seen = set([(start[1], start[0])])
    while not q.empty():
        path = q.get()
        x, y = path[-1]
        if (y, x) == end:
            distance = len(path) - 1
            print(
                f"The distance between galaxy {galaxies.index(start) + 1} and galaxy {galaxies.index(end) + 1} is: {distance}"
            )
            return distance
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= x2 < width and 0 <= y2 < height and (x2, y2) not in seen:
                q.put(path + [(x2, y2)])
                seen.add((x2, y2))


total_distance = 0
distances = {}
for i, galaxy in enumerate(galaxies):
    for j, other_galaxy in enumerate(galaxies[i + 1 :]):
        total_distance += bfs(galaxy, other_galaxy)

print(f"The sum of the shortest path between every pair of galaxies is: {total_distance}")
