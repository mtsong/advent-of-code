import pathlib
import re


USE_EXAMPLE = False
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
    arrangements = list(arrange(springs))
    pattern = re.compile(rf"^\.*{r"\.+".join([f"#{{{c}}}" for c in config.split(",")])}\.*$")
    print(f"Checking {len(arrangements)} arrangements for {springs} and {config}")
    for arrangement in arrangements:
        if is_valid(arrangement, pattern):
            total_arrangements += 1
print(f"The number of possible arrangements is: {total_arrangements}")
