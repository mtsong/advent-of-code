from collections import defaultdict
import re
from typing import Iterator, NamedTuple


DAY = 3
USE_EXAMPLE = False


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(code: str) -> Iterator[Token]:
    token_specification = [("NUMBER", r"\d+"), ("SYMBOL", r"[^\.\d\s]"), ("PERIOD", r"\.+"), ("NEWLINE", r"\n")]
    token_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for match_object in re.finditer(token_regex, code):
        kind = match_object.lastgroup
        value = match_object.group()
        column = match_object.start() - line_start
        if kind == "NUMBER":
            value = int(value)
        elif kind == "NEWLINE":
            line_start = match_object.end()
            line_num += 1
            continue
        elif kind == "PERIOD":
            continue
        yield Token(kind, value, line_num, column)


with open(f"{DAY}/example.txt" if USE_EXAMPLE else f"{DAY}/input.txt", encoding="utf-8") as f:
    data = f.read()


tokenized_data = list(tokenize(data))

# Get numbers for each line
numbers_by_line = defaultdict(list)
for token in tokenized_data:
    if token.type == "NUMBER":
        numbers_by_line[token.line].append(token)

# For each number, see if there's a symbol in matching range and add to answer if so
answer = 0
num_gears = 0
for token in tokenized_data:
    if token.value == "*":
        start_line = token.line - 1 if token.line > 1 else 1
        end_line = token.line + 1
        start_column = token.column - 1 if token.column > 0 else 0
        end_column = token.column + 1
        adjacent_numbers = []
        for line in range(start_line, end_line + 1):
            for number in numbers_by_line[line]:
                number_width = len(str(number.value))
                number_end_column = number.column + number_width - 1
                if (
                    token.column == number.column
                    or number.column <= start_column <= number_end_column
                    or number.column <= end_column <= number_end_column
                ):
                    adjacent_numbers.append(number)
        if len(adjacent_numbers) == 2:
            # print(f"Gear found at {token.line},{token.column} with part numbers {[a.value for a in adjacent_numbers]}")
            num_gears += 1
            answer += adjacent_numbers[0].value * adjacent_numbers[1].value
        else:
            print(f"No gear found at {token.line},{token.column}")
print(num_gears)
print(answer)
