import pathlib

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
nodes = {}
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    instructions = ""
    for i, line in enumerate(f):
        parts = line.split("=")
        if i == 0:
            instructions = line.strip()
        elif i == 1:
            continue
        else:
            node, elements = line.split("=")
            nodes[node.strip()] = tuple(e.strip() for e in elements.strip("\n ()").split(","))

steps = 0
element = "AAA"
while element != "ZZZ":
    print(element)
    instruction = instructions[steps % len(instructions)]
    element = nodes[element][instruction == "R"]
    steps += 1
print(f"{steps} steps required to go from AAA to ZZZ")
