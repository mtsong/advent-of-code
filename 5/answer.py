import pathlib

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.read()


def parse_map(map):
    special_mappings = {}
    for line in map.split("\n"):
        if not line:
            continue
        dest_start, source_start, range_len = line.split()
        dest_start = int(dest_start)
        source_start = int(source_start)
        range_len = int(range_len)
        for i in range(source_start, source_start + range_len):
            special_mappings[i] = dest_start + i - source_start
    return special_mappings


sections = lines.split("\n\n")
seeds = [int(seed) for seed in sections[0].split(":")[1].split()]
maps = []
for section in sections[1:]:
    name, map = section.split(":")
    maps.append((name.split()[0].split("-")[2], parse_map(map)))

locations = []
next_lookup = 0
for seed in seeds:
    next_lookup = seed
    route = []
    category = "seed"
    for category, map in maps:
        next_lookup = map.get(next_lookup, next_lookup)
        route.append(f"{category} {next_lookup}")
    locations.append(next_lookup)
    print(", ".join(route))
print(f"The lowest location number is {min(locations)}")
