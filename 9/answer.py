import pathlib

USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    histories = []
    for line in f:
        histories.append([int(n) for n in line.split()])

total_previous_values = 0
for history in histories:
    original_history = history
    sequences = [history]
    while set(history) != {0}:
        print(history)
        diffs = []
        for i, value in enumerate(history):
            if i < len(history) - 1:
                diffs.append(history[i + 1] - value)
        else:
            history = diffs
            sequences.append(history)
    previous_value = 0
    while sequences:
        previous_value = sequences.pop()[0] - previous_value
    total_previous_values += previous_value
    print(f"The previous value of {original_history} is {previous_value}")
print(f"The sum of these extrapolated values is {total_previous_values}")
