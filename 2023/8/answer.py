import pathlib
import math

USE_EXAMPLE = False
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

element_steps = []
elements = tuple(node for node in nodes.keys() if node.endswith("A"))
dest_elements = []
for element in elements:
    steps = 0
    orig_element = element
    while not element.endswith("Z"):
        instruction = instructions[steps % len(instructions)]
        element = nodes[element][instruction == "R"]
        steps += 1
    dest_elements.append(element)
    print(f"{steps} steps required to go from {orig_element} to {element}")
    element_steps.append(steps)
print(f"{math.lcm(*element_steps)} steps required to go from {elements} to {tuple(dest_elements)}")
