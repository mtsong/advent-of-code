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
seed_defs = sections[0].split(":")[1].split()
for i, seed_range in enumerate(seed_defs):
    if i % 2 == 0:
        seeds.append((range(int(seed_range), int(seed_range) + int(seed_defs[i + 1]))))
print(f"Found {sum(len(seed) for seed in seeds):,} seeds")

maps = []
for section in sections[1:]:
    name, map = section.split(":")
    maps.append((name.split()[0].split("-")[2], parse_map(map)))

routes = []
for category, map in maps:
    ranges = {}
    for dest_start, source_start, range_len in map:
        dest_range = range(dest_start, dest_start + range_len)
        source_range = range(source_start, source_start + range_len)
        ranges[source_range] = dest_range
    routes.append((category, ranges))

min_location = sys.maxsize
for seed_range in seeds:
    prev_category = "seed"
    prev_seed_range = seed_range
    for category, ranges in routes:
        print(f"Checking {prev_category} {seed_range} in {category}")
        for source_range, dest_range in ranges.items():
            intersection = range_intersect(seed_range, source_range)
            if intersection is not None:
                print(f"{prev_category} {seed_range} is in {category} {source_range}")
                if category == "location":
                    break
                dest_range_start = intersection.start - source_range.start
                dest_range_end = intersection.stop - source_range.start
                dest_range = range_intersect(
                    range(dest_range_start + dest_range.start, dest_range_end + dest_range.start), dest_range
                )
                seed_range = dest_range
                break
            else:
                print(f"{prev_category} {seed_range} is not in {category} {source_range}")
        prev_category = category
        prev_seed_range = seed_range
        if category == "location":
            location = min(seed_range.start, prev_seed_range.start)
            if min(seed_range.start, prev_seed_range.start) < min_location:
                min_location = location
    print("==============================")
print(f"The lowest location number that corresponds to any of the initial seed numbers is {min_location}")
