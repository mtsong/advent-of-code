import pathlib
import re
import itertools
import exrex


USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = [line.strip().split() for line in f]


def is_valid(arrangement, pattern):
    return pattern.match(arrangement)


def arrange(springs):
    if "?" not in springs:
        yield springs
    else:
        yield from arrange(springs.replace("?", ".", 1))
        yield from arrange(springs.replace("?", "#", 1))


total_arrangements = 0
for springs, config in lines:
    # springs = "?".join(itertools.repeat(springs, 5))
    config = config.split(",")
    leading_dots = len(springs) - len(springs.lstrip("."))
    trailing_dots = len(springs) - len(springs.rstrip("."))
    valid_arrangements = list(
        exrex.generate(
            rf"^\.{{{leading_dots}}}{r"\.+".join([f"#{{{c}}}" for c in config])}\.{{{trailing_dots}}}$",
            1,
        )
    )
    if len(valid_arrangements) == 1:
        print(f"The only valid arrangement for {springs} and {config} is:")
        print(f"{valid_arrangements[0]}\n")
        total_arrangements += 1
    else:
        print(f"There are {len(valid_arrangements)} possible arrangements for {springs} and {config}\n")
        total_arrangements += len(valid_arrangements)
print(f"The number of possible arrangements is: {total_arrangements}")
