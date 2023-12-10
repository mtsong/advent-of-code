import pathlib
from dataclasses import dataclass

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:

    @dataclass
    class Tile:
        x: int | None = None
        y: int | None = None
        c: str | None = None

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

# loop = False
# current_tile = start_tile
# while not loop:
#     adjacent_tiles = get_adjacent_tiles(current_tile)
#     for i, tile in enumerate(adjacent_tiles):
#         print(i, tile)
#     break
