import re
import pathlib

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = f.readlines()

non_digits = re.compile(r"[^\d]")
time = int(non_digits.sub("", lines[0].split(":")[1]))
record = int(non_digits.sub("", lines[1].split(":")[1]))

ways = 0
for button in range(time):
    distance = (time - button) * button
    if distance > record:
        print(f"Holding the button for {button} results in {distance} mm which is more than {record}")
        ways += 1

print(f"Answer: {ways}")
