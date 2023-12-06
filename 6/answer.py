import pathlib

USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.readlines()

times = [int(t) for t in lines[0].split(":")[1].split()]
records = [int(d) for d in lines[1].split(":")[1].split()]

total_ways = 1
for time, record in zip(times, records):
    ways = 0
    for button in range(time):
        distance = (time - button) * button
        if distance > record:
            print(f"Holding the button for {button} results in {distance} mm which is more than {record}")
            ways += 1
    total_ways *= ways

print(f"Answer: {total_ways}")
