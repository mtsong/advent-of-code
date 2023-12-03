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

# Get symbols for each line
symbol_by_line = defaultdict(list)
for token in tokenized_data:
    if token.type == "SYMBOL":
        symbol_by_line[token.line].append(token)

# For each number, see if there's a symbol in matching range and add to answer if so
answer = 0
for token in tokenized_data:
    if token.type == "NUMBER":
        start_line = token.line - 1 if token.line > 1 else 1
        end_line = token.line + 1
        start_column = token.column - 1 if token.column > 0 else 0
        end_column = token.column + len(str(token.value))
        for line in range(start_line, end_line + 1):
            part_valid = False
            for symbol in symbol_by_line[line]:
                if start_column <= symbol.column <= end_column:
                    answer += token.value
                    print(f"Valid part: {token.value}")
                    part_valid = True
                    break
            if part_valid:
                break
print(answer)
