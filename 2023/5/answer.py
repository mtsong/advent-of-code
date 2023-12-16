import pathlib
import sys

USE_EXAMPLE = False
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


def follow_route(input_range, next_route_index):
    global location, min_location

    route = routes[next_route_index]
    category = route[0]
    new_ranges = set()
    remaining_input_range = input_range
    for source_range, dest_range in route[1].items():
        intersection = range_intersect(input_range, source_range)
        if intersection is not None:
            new_ranges.add(
                range(
                    dest_range.start + intersection.start - source_range.start,
                    dest_range.start + intersection.stop - source_range.start,
                )
            )
            if intersection == input_range:
                remaining_input_range = None
                break
            else:
                # Remove the intersecting numbers from input_range
                if intersection.start > input_range.start:
                    remaining_input_range = range(remaining_input_range.start, intersection.start)
                elif intersection.stop < input_range.stop:
                    remaining_input_range = range(intersection.stop, remaining_input_range.stop)
    if remaining_input_range is not None:
        new_ranges.add(remaining_input_range)
    if not new_ranges:
        new_ranges = {input_range}
    for new_range in new_ranges:
        if next_route_index == len(routes) - 1:
            if new_range.start < location:
                location = new_range.start
        else:
            follow_route(new_range, next_route_index + 1)


min_location = sys.maxsize
location = sys.maxsize
for seed_range in seeds:
    follow_route(seed_range, 0)
    print(f"Minimum location for seed {seed_range} is {location}")
    if location < min_location:
        min_location = location
    location = sys.maxsize
    print("========================================")
print(f"The lowest location number that corresponds to any of the initial seed numbers is {min_location}")


"""
Found 27 seeds
seed 79 -> soil 81 -> fertilizer 81 -> water 81 -> light 74 -> temperature 78 -> humidity 78 -> location 82
seed 80 -> soil 82 -> fertilizer 82 -> water 82 -> light 75 -> temperature 79 -> humidity 79 -> location 83
seed 81 -> soil 83 -> fertilizer 83 -> water 83 -> light 76 -> temperature 80 -> humidity 80 -> location 84
seed 82 -> soil 84 -> fertilizer 84 -> water 84 -> light 77 -> temperature 45 -> humidity 46 -> location 46
seed 83 -> soil 85 -> fertilizer 85 -> water 85 -> light 78 -> temperature 46 -> humidity 47 -> location 47
seed 84 -> soil 86 -> fertilizer 86 -> water 86 -> light 79 -> temperature 47 -> humidity 48 -> location 48
seed 85 -> soil 87 -> fertilizer 87 -> water 87 -> light 80 -> temperature 48 -> humidity 49 -> location 49
seed 86 -> soil 88 -> fertilizer 88 -> water 88 -> light 81 -> temperature 49 -> humidity 50 -> location 50
seed 87 -> soil 89 -> fertilizer 89 -> water 89 -> light 82 -> temperature 50 -> humidity 51 -> location 51
seed 88 -> soil 90 -> fertilizer 90 -> water 90 -> light 83 -> temperature 51 -> humidity 52 -> location 52
seed 89 -> soil 91 -> fertilizer 91 -> water 91 -> light 84 -> temperature 52 -> humidity 53 -> location 53
seed 90 -> soil 92 -> fertilizer 92 -> water 92 -> light 85 -> temperature 53 -> humidity 54 -> location 54
seed 91 -> soil 93 -> fertilizer 93 -> water 93 -> light 86 -> temperature 54 -> humidity 55 -> location 55
seed 92 -> soil 94 -> fertilizer 94 -> water 94 -> light 87 -> temperature 55 -> humidity 56 -> location 60
Minimum location for seed range(79, 93) is 46
seed 55 -> soil 57 -> fertilizer 57 -> water 53 -> light 46 -> temperature 82 -> humidity 82 -> location 86
seed 56 -> soil 58 -> fertilizer 58 -> water 54 -> light 47 -> temperature 83 -> humidity 83 -> location 87
seed 57 -> soil 59 -> fertilizer 59 -> water 55 -> light 48 -> temperature 84 -> humidity 84 -> location 88
seed 58 -> soil 60 -> fertilizer 60 -> water 56 -> light 49 -> temperature 85 -> humidity 85 -> location 89
seed 59 -> soil 61 -> fertilizer 61 -> water 61 -> light 54 -> temperature 90 -> humidity 90 -> location 94
seed 60 -> soil 62 -> fertilizer 62 -> water 62 -> light 55 -> temperature 91 -> humidity 91 -> location 95
seed 61 -> soil 63 -> fertilizer 63 -> water 63 -> light 56 -> temperature 92 -> humidity 92 -> location 96
seed 62 -> soil 64 -> fertilizer 64 -> water 64 -> light 57 -> temperature 93 -> humidity 93 -> location 56
seed 63 -> soil 65 -> fertilizer 65 -> water 65 -> light 58 -> temperature 94 -> humidity 94 -> location 57
seed 64 -> soil 66 -> fertilizer 66 -> water 66 -> light 59 -> temperature 95 -> humidity 95 -> location 58
seed 65 -> soil 67 -> fertilizer 67 -> water 67 -> light 60 -> temperature 96 -> humidity 96 -> location 59
seed 66 -> soil 68 -> fertilizer 68 -> water 68 -> light 61 -> temperature 97 -> humidity 97 -> location 97
seed 67 -> soil 69 -> fertilizer 69 -> water 69 -> light 62 -> temperature 98 -> humidity 98 -> location 98
Minimum location for seed range(55, 68) is 56
The lowest location number is 46
"""
