import re
import pathlib

USE_EXAMPLE = False
PART_1 = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.readlines()

non_digits = re.compile(r"[^\d]")

if PART_1:
    times = [int(t) for t in lines[0].split(":")[1].split()]
    records = [int(d) for d in lines[1].split(":")[1].split()]
else:
    times = [int(non_digits.sub("", lines[0].split(":")[1]))]
    records = [int(non_digits.sub("", lines[1].split(":")[1]))]

total_ways = 1
for time, record in zip(times, records):
    ways = 0
    for button in range(time):
        distance = (time - button) * button
        if distance > record:
            print(f"Holding the button for {button} seconds results in {distance} mm which is more than {record}")
            ways += time + 1 - button * 2
            print(f"Found {ways} ways to beat the record of {record} mm")
            break
    total_ways *= ways

print(f"Answer: {total_ways}")
