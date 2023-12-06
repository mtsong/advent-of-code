import pathlib
import sys

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.read()


def range_intersect(range1: range, range2: range) -> range | None:
    return range(max(range1.start, range2.start), min(range1.stop, range2.stop)) or None


def parse_map(map: str) -> list[tuple[int, int, int]]:
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
seeds = []
seed_ranges = sections[0].split(":")[1].split()
for i, seed_range in enumerate(seed_ranges):
    if i % 2 == 0:
        seeds.append((range(int(seed_range), int(seed_range) + int(seed_ranges[i + 1]))))
print(f"Found {sum(len(seed) for seed in seeds)} seeds")

maps = []
for section in sections[1:]:
    name, map = section.split(":")
    maps.append((name.split()[0].split("-")[2], parse_map(map)))


min_location = sys.maxsize


def find_location(key, maps, category):
    global min_location
    if not maps:
        return key
    original_key = key
    route = [f"{category} {key}"]
    map_index = None
    for i, (category, map) in enumerate(maps):
        special_ranges = []
        for map_range in map:
            dest_start, source_start, range_len = map_range
            source_range = range(source_start, source_start + range_len)
            dest_range = range(dest_start, dest_start + range_len)
            special_ranges.append((source_range, dest_range))

        for special_range in special_ranges:
            if key in special_range[0]:
                key = special_range[1][key - special_range[0][0]]
                if map_index is None:
                    map_index = i
                    original_key = key
                break
        route.append(f"{category} {key}")
    if key < min_location:
        min_location = key
    print(", ".join(route))
    if map_index is None:
        return find_location(key + 1, maps, category)
    return find_location(original_key + 1, maps[map_index + 1 :], maps[map_index][0])


min_location = sys.maxsize
for seed_range in seeds:
    location = find_location(seed_range[0], maps, "seed")
    if location < min_location:
        min_location = location
print(f"The lowest location number is {min_location}")
