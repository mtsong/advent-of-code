import pathlib
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Tile:
    x: int | None = None
    y: int | None = None
    c: str | None = None


USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    map = []
    for i, line in enumerate(f):
        row = []
        for j, character in enumerate(line):
            tile = Tile(j, i, character)
            row.append(tile)
            if tile.c == "S":
                start_tile = tile
        map.append(row)

width = len(map[0])
height = len(map)


def get_adjacent_tiles(tile: Tile) -> list[Tile]:
    adjacent_tiles = []
    ground = Tile()
    # West
    if tile.x > 0:
        adjacent_tiles.append(Tile(tile.x - 1, tile.y, map[tile.y][tile.x - 1].c))
    else:
        adjacent_tiles.append(ground)
    # North
    if tile.y > 0:
        adjacent_tiles.append(Tile(tile.x, tile.y - 1, map[tile.y - 1][tile.x].c))
    else:
        adjacent_tiles.append(ground)
    # East
    if tile.x < width - 1:
        adjacent_tiles.append(Tile(tile.x + 1, tile.y, map[tile.y][tile.x + 1].c))
    else:
        adjacent_tiles.append(ground)
    # South
    if tile.y < height - 1:
        adjacent_tiles.append(Tile(tile.x, tile.y + 1, map[tile.y + 1][tile.x].c))
    else:
        adjacent_tiles.append(ground)
    return adjacent_tiles


adjacent_start_tiles = get_adjacent_tiles(start_tile)
if adjacent_start_tiles[0].c in ("-", "L", "F"):
    if adjacent_start_tiles[1].c in ("|", "7", "F"):
        start_tile.c = "J"
    elif adjacent_start_tiles[2].c in ("-", "J", "7"):
        start_tile.c = "-"
    elif adjacent_start_tiles[3].c in ("|", "L", "J"):
        start_tile.c = "7"
elif adjacent_start_tiles[1].c in ("|", "7", "F"):
    if adjacent_start_tiles[0].c in ("-", "L", "F"):
        start_tile.c = "J"
    elif adjacent_start_tiles[2].c in ("-", "J", "7"):
        start_tile.c = "L"
    elif adjacent_start_tiles[3].c in ("|", "L", "J"):
        start_tile.c = "|"
elif adjacent_start_tiles[2].c in ("-", "7", "J"):
    if adjacent_start_tiles[0].c in ("-", "F", "L"):
        start_tile.c = "-"
    elif adjacent_start_tiles[1].c in ("|", "7", "F"):
        start_tile.c = "L"
    if adjacent_start_tiles[3].c in ("|", "L", "J"):
        start_tile.c = "F"
elif adjacent_start_tiles[3].c in ("|", "L", "J"):
    if adjacent_start_tiles[0].c in ("-", "L", "F"):
        start_tile.c = "7"
    elif adjacent_start_tiles[1].c in ("|", "7", "F"):
        start_tile.c = "|"
    if adjacent_start_tiles[2].c in ("-", "J", "7"):
        start_tile.c = "F"

print(f"Start tile: {start_tile}")

if start_tile.c == "|":
    route_starts = (map[start_tile.y - 1][start_tile.x], map[start_tile.y + 1][start_tile.x])
elif start_tile.c == "-":
    route_starts = (map[start_tile.y][start_tile.x - 1], map[start_tile.y][start_tile.x + 1])
elif start_tile.c == "L":
    route_starts = (map[start_tile.y - 1][start_tile.x], map[start_tile.y][start_tile.x + 1])
elif start_tile.c == "J":
    route_starts = (map[start_tile.y - 1][start_tile.x], map[start_tile.y][start_tile.x - 1])
elif start_tile.c == "7":
    route_starts = (map[start_tile.y + 1][start_tile.x], map[start_tile.y][start_tile.x - 1])
elif start_tile.c == "F":
    route_starts = (map[start_tile.y + 1][start_tile.x], map[start_tile.y][start_tile.x + 1])


def get_direction(previous: Tile, current: Tile) -> str:
    x_diff = current.x - previous.x
    y_diff = current.y - previous.y
    if x_diff == 1:
        return "E"
    if x_diff == -1:
        return "W"
    if y_diff == 1:
        return "S"
    return "N"


def navigate(previous: Tile, current: Tile) -> Tile:
    direction = get_direction(previous, current)
    x, y = current.x, current.y
    if current.c == "|":
        if direction == "N":
            y = current.y - 1
        else:
            y = current.y + 1
    elif current.c == "-":
        if direction == "E":
            x = current.x + 1
        else:
            x = current.x - 1
    if current.c == "L":
        if direction == "S":
            x = current.x + 1
        else:
            y = current.y - 1
    if current.c == "J":
        if direction == "S":
            x = current.x - 1
        else:
            y = current.y - 1
    if current.c == "7":
        if direction == "E":
            y = current.y + 1
        else:
            x = current.x - 1
    if current.c == "F":
        if direction == "N":
            x = current.x + 1
        else:
            y = current.y + 1
    return map[y][x]


prev_tile = start_tile
current_tile = route_starts[0]
route = [start_tile, current_tile]
while current_tile != start_tile:
    next_tile = navigate(prev_tile, current_tile)
    prev_tile = current_tile
    current_tile = next_tile
    route.append(current_tile)

min_x = min(route, key=lambda tile: tile.x).x
max_x = max(route, key=lambda tile: tile.x).x
min_y = min(route, key=lambda tile: tile.y).y
max_y = max(route, key=lambda tile: tile.y).y


def within_bounds(tile: Tile) -> bool:
    if tile.x is None or tile.y is None:
        return False
    return min_x <= tile.x <= max_x and min_y <= tile.y <= max_y


route_tiles = set(route)


possible_enclosed = set()
for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        tile = map[y][x]
        if tile not in route_tiles:
            possible_enclosed.add(tile)

possible_closed_regions = []
while possible_enclosed:
    current_tile = possible_enclosed.pop()
    region = {current_tile}
    adjacent_tiles = get_adjacent_tiles(current_tile)
    next_adjacent_tiles = set(adjacent_tiles)
    while next_adjacent_tiles:
        tile = next_adjacent_tiles.pop()
        if within_bounds(tile) and tile not in route:
            region.add(tile)
            possible_enclosed.discard(tile)
            adjacent_tiles = get_adjacent_tiles(tile)
            nat = {
                t for t in adjacent_tiles if t.c is not None and within_bounds(t) and t not in region and t not in route
            }
            next_adjacent_tiles |= nat
    possible_closed_regions.append(region)


def get_navigable_pairs(tile: Tile) -> tuple[str, list[tuple[Tile, Tile]]]:
    west, north, east, south = get_adjacent_tiles(tile)
    pairs = []
    direction = "W"
    # West and northwest
    if west.c == "-" and map[west.y - 1][west.x].c in ("-", "L", "J"):
        pairs.append((west, map[west.y - 1][west.x]))
    # West and southwest
    elif west.c == "-" and map[west.y + 1][west.x].c in ("-", "F", "7"):
        pairs.append((map[west.y + 1][west.x], west))
    # North and northwest
    elif north.c == "|" and map[north.y][north.x - 1].c in ("|", "7", "J"):
        direction = "N"
        pairs.append((map[north.y][north.x - 1], north))
    # North and northeast
    elif north.c == "|" and map[north.y][north.x + 1].c in ("|", "L", "F"):
        direction = "N"
        pairs.append((north, map[north.y][north.x + 1]))
    # East and northeast
    elif east.c == "-" and map[east.y - 1][east.x].c in ("-", "L", "J"):
        direction = "E"
        pairs.append((map[east.y - 1][east.x], east))
    # East and southeast
    elif east.c == "-" and map[east.y + 1][east.x].c in ("-", "F", "7"):
        direction = "E"
        pairs.append((east, map[east.y + 1][east.x]))
    # South and southeast
    elif south.c in ("7", "|") and map[south.y][south.x + 1].c in ("|", "F", "L"):
        direction = "S"
        pairs.append((south, map[south.y][south.x + 1]))
    # South and southwest
    elif south.c in ("7", "|", "F") and map[south.y][south.x - 1].c in ("|", "7", "J", "."):
        direction = "S"
        pairs.append((map[south.y][south.x - 1], south))
    return direction, pairs


def is_navigable_pair(direction: str, tile_1: Tile, tile_2: Tile) -> str | None:
    # Parallel pipes
    if direction in ("N", "S") and tile_1.c in ("7", "|", "J", ".") and tile_2.c in ("|", "F", "L", "."):
        return direction
    if direction in ("E", "W") and tile_1.c in ("-", "L", "J") and tile_2.c in ("-", "F", "7"):
        return direction
    # West right turn
    if direction == "W" and tile_1.c in ("|", "7", "J") and tile_2.c in ("-", "L", "J"):
        return "N"
    # West left turn
    if direction == "W" and tile_1.c in ("|", "7", "J") and tile_2.c in ("-", "F", "7"):
        return "S"
    # North right turn
    if direction == "N" and tile_1.c in ("-", "L", "J") and tile_2.c in ("|", "F", "L"):
        return "E"
    # North left turn
    if direction == "N" and tile_1.c in ("-", "L", "J") and tile_2.c in ("|", "7", "J"):
        return "W"
    # East right turn
    if direction == "E" and tile_1.c in ("|", "F", "L") and tile_2.c in ("-", "F", "7"):
        return "S"
    # East left turn
    if direction == "E" and tile_1.c in ("|", "F", "L") and tile_2.c in ("-", "L", "J"):
        return "N"
    # South right turn
    if direction == "S" and tile_1.c in ("-", "F", "7") and tile_2.c in ("|", "7", "J"):
        return "W"
    # South left turn
    if direction == "S" and tile_1.c in ("-", "F", "7") and tile_2.c in ("|", "F", "L"):
        return "E"
    return None


def can_exit(direction: str, tile_1: Tile, tile_2: Tile) -> bool:
    while within_bounds(tile_1) and within_bounds(tile_2):
        direction = is_navigable_pair(direction, tile_1, tile_2)
        if direction is None:
            return False
        if direction == "S":
            if tile_1.y == max_y or tile_2.y == max_y:
                return True
            tile_1 = map[tile_1.y + 1][tile_1.x]
            tile_2 = map[tile_2.y + 1][tile_2.x]
        elif direction == "N":
            if tile_1.y == min_y or tile_2.y == min_y:
                return True
            tile_1 = map[tile_1.y - 1][tile_1.x]
            tile_2 = map[tile_2.y - 1][tile_2.x]
        elif direction == "E":
            if tile_1.x == max_x or tile_2.x == max_x:
                return True
            tile_1 = map[tile_1.y][tile_1.x + 1]
            tile_2 = map[tile_2.y][tile_2.x + 1]
        else:
            if tile_1.x == min_x or tile_2.x == min_x:
                return True
            tile_1 = map[tile_1.y][tile_1.x - 1]
            tile_2 = map[tile_2.y][tile_2.x - 1]
    return True


all_possible_enclosed = set.union(*possible_closed_regions) | route_tiles


def get_diagonal_tiles(tile: Tile) -> list[Tile]:
    diagonal_tiles = []
    ground = Tile()
    # Northwest
    if tile.x > 0 and tile.y > 0:
        diagonal_tiles.append(Tile(tile.x - 1, tile.y - 1, map[tile.y - 1][tile.x - 1].c))
    else:
        diagonal_tiles.append(ground)
    # Northeast
    if tile.y > 0 and tile.x < width - 1:
        diagonal_tiles.append(Tile(tile.x + 1, tile.y - 1, map[tile.y - 1][tile.x + 1].c))
    else:
        diagonal_tiles.append(ground)
    # Southeast
    if tile.x < width - 1 and tile.y < height - 1:
        diagonal_tiles.append(Tile(tile.x + 1, tile.y + 1, map[tile.y + 1][tile.x + 1].c))
    else:
        diagonal_tiles.append(ground)
    # Southwest
    if tile.y < height - 1 and tile.x > 0:
        diagonal_tiles.append(Tile(tile.x - 1, tile.y + 1, map[tile.y + 1][tile.x - 1].c))
    else:
        diagonal_tiles.append(ground)
    return diagonal_tiles


def is_enclosed(region: set[Tile]) -> bool:
    for tile in region:
        adjacent_tiles = get_adjacent_tiles(tile)
        diagonal_tiles = get_diagonal_tiles(tile)
        for t in adjacent_tiles + diagonal_tiles:
            if not within_bounds(t) or t.c is None or t not in all_possible_enclosed:
                return False
        direction, navigable_pairs = get_navigable_pairs(tile)
        if navigable_pairs:
            for pair in navigable_pairs:
                if can_exit(direction, pair[0], pair[1]):
                    return False
    return True


enclosed_area = 0
pretty_map = []
for row in map:
    pretty_row = []
    for tile in row:
        if tile not in route_tiles:
            pretty_row.append(Tile(tile.x, tile.y, "."))
        else:
            if tile.c == "-":
                pretty_row.append(Tile(tile.x, tile.y, "―"))
            elif tile.c == "L":
                pretty_row.append(Tile(tile.x, tile.y, "╰"))
            elif tile.c == "J":
                pretty_row.append(Tile(tile.x, tile.y, "╯"))
            elif tile.c == "7":
                pretty_row.append(Tile(tile.x, tile.y, "╮"))
            elif tile.c == "F":
                pretty_row.append(Tile(tile.x, tile.y, "╭"))
            else:
                pretty_row.append(tile)
    pretty_map.append(pretty_row)

for region in possible_closed_regions:
    if is_enclosed(region):
        enclosed_area += len(region)
        for tile in region:
            pretty_map[tile.y][tile.x].c = "I"
    else:
        for tile in region:
            pretty_map[tile.y][tile.x].c = "."
for row in pretty_map:
    print("".join(t.c for t in row))
print(f"Enclosed area: {enclosed_area}")
