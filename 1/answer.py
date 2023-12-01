import re

digit = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine|ten))")

word_to_num = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

sum = 0
with open("1/input.txt", encoding="utf-8") as f:
    for line in f:
        digits = digit.findall(line)
        if digits:
            first_match = digits[0]
            if not first_match.isnumeric():
                first_match = word_to_num[first_match]
            last_match = digits[-1]
            if not last_match.isnumeric():
                last_match = word_to_num[last_match]
            print(f"{line[:-1]} = {first_match}{last_match}")
            sum += int(first_match + last_match)
    print(sum)
