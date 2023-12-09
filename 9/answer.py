import pathlib

USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    histories = []
    for line in f:
        histories.append([int(n) for n in line.split()])

total_next_value = 0
for history in histories:
    original_history = history
    sequences = [history]
    found = False
    while history and not found:
        print(history)
        diffs = []
        reversed_history = list(reversed(history))
        for i, value in enumerate(reversed_history):
            if i < len(reversed_history) - 1:
                diff_with_previous = value - reversed_history[i + 1]
                if i == 1 and diff_with_previous == diffs[i - 1]:
                    next_value = diff_with_previous
                    while sequences:
                        next_value = sequences.pop()[-1] + next_value
                    total_next_value += next_value
                    found = True
                    break
                diffs.append(diff_with_previous)
        else:
            history = list(reversed(diffs))
            sequences.append(history)
    print(f"The next value of {original_history} is {next_value}")
print(f"The sum of these extrapolated values is {total_next_value}")
