import pathlib

USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.read()


def parse_map(map):
    special_mappings = []
    for line in map.split("\n"):
        if not line:
            continue
        dest_start, source_start, range_len = line.split()
        dest_start = int(dest_start)
        source_start = int(source_start)
        range_len = int(range_len)
        special_mappings.append((dest_start, source_start, range_len))
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
        special_ranges = []
        for map_range in map:
            dest_start, source_start, range_len = map_range
            source_range = range(source_start, source_start + range_len)
            dest_range = range(dest_start, dest_start + range_len)
            special_ranges.append((source_range, dest_range))

        for special_range in special_ranges:
            if next_lookup in special_range[0]:
                next_lookup = special_range[1][next_lookup - special_range[0][0]]
                break
        route.append(f"{category} {next_lookup}")
    locations.append(next_lookup)
    print(", ".join(route))
print(f"The lowest location number is {min(locations)}")
