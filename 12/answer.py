import pathlib
import re
import itertools
import exrex


USE_EXAMPLE = True
CWD = pathlib.Path(__file__).parent.resolve()
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    lines = [line.strip().split() for line in f]


def is_valid(arrangement, pattern):
    return pattern.match(arrangement)


def arrange(springs):
    if "?" not in springs:
        yield springs
    else:
        yield from arrange(springs.replace("?", ".", 1))
        yield from arrange(springs.replace("?", "#", 1))


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


total_arrangements = 0
for springs, config in lines:
    # springs = "?".join(itertools.repeat(springs, 5))
    config = [int(c) for c in config.split(",")]
    i = 0
    arrangements = 0
    for c, next_c in pairwise(config):
        min_chars = c + next_c + 1
        possible_spring_count = 0
        # TODO: Split into groups and count the number of #s and ?s in each group and check against min chars
        while i < len(springs) and possible_spring_count < min_chars:
            if springs[i] in ("#", "?"):
                possible_spring_count += 1
            i += 1
            if i >= len(springs):
                break
        if possible_spring_count == min_chars:
            arrangements += 1
    print(f"The number of arrangements for {springs} and {config} is: {arrangements}")
    total_arrangements += arrangements

    # i = 0
    # max_q_count = 0
    # for c in config:
    #     spring_count = 0
    #     q_count = 0
    #     prev_char = "."
    #     possible_positions = 0
    #     while i < len(springs) and spring_count < c:
    #         s = springs[i]
    #         while s == prev_char:
    #             if s == "#":
    #                 spring_count += 1
    #             elif s == "?":
    #                 q_count += 1
    #                 if q_count > max_q_count:
    #                     max_q_count = q_count
    #             i += 1
    #             if i >= len(springs):
    #                 break
    #             s = springs[i]
    #         if s == "#":
    #             spring_count += 1
    #         elif s == "?":
    #             q_count += 1
    #             if q_count > max_q_count:
    #                 max_q_count = q_count
    #             if q_count == c:
    #                 possible_positions = q_count
    #                 break
    #         i += 1
    #     dot_count = 0
    #     while i < len(springs) and springs[i] in ("?", "."):
    #         if springs[i] == ".":
    #             dot_count += 1
    #         i += 1
    #         if i < len(springs) and springs[i] == "?":
    #             break
    # print(f"The number of arrangements for {springs} and {config} is: {max_q_count}")
    # total_arrangements += max_q_count
    # leading_dots = len(springs) - len(springs.lstrip("."))
    # trailing_dots = len(springs) - len(springs.rstrip("."))
    # leading_qs = len(springs) - len(springs.lstrip("?"))
    # trailing_qs = len(springs) - len(springs.rstrip("?"))
    # pattern = r"^\.*"
    # i = 0
    # possible_positions = 1
    # for c in config:
    #     c = int(c)
    #     spring_count = 0
    #     while i < len(springs) and spring_count != c:
    #         s = springs[i]
    #         if s in ("#", "?"):
    #             if spring_count > 0 or s == "#":
    #                 spring_count += 1
    #             elif spring_count == 0 and s == "?":
    #                 spring_count += 1
    #         i += 1
    #     pattern += f"#{{{spring_count}}}"
    #     # Need at least one dot before the next group
    #     dot_count = 0
    #     while i < len(springs) and springs[i] in ("?", "."):
    #         if springs[i] == ".":
    #             dot_count += 1
    #         else:
    #             possible_positions += 1
    #         i += 1
    #         while i < len(springs) and springs[i] == "?":
    #             i += 1
    #             possible_positions += 1
    #     if i < len(springs):
    #         pattern += rf"\.{{{dot_count}}}"
    #     possible_positions /= c

    # valid_arrangements = list(exrex.generate(pattern, 1))
    # if len(valid_arrangements[0]) <= len(springs) <= len(valid_arrangements[0]) + leading_qs + trailing_qs:
    #     print(f"There are {possible_positions} possible arrangements for {springs} and {config}")
    #     total_arrangements += leading_qs + trailing_qs
    # else:
    #     # Find indexes of #s and ?s and add up the difference in length of these (maybe do some multiplication)
    #     q_indexes = [m.span(1) for m in re.finditer(r"\.*([\?\#]+)\.*", springs)]
    #     arrangements = 0
    #     for i, qi in enumerate(q_indexes):
    #         # Get number of question marks in source string for this range
    #         num_qs = springs[qi[0] : qi[1]].count("?")
    #         arrangements += (qi[1] - qi[0] - num_qs) * 2
    #     print(f"There are {arrangements} possible arrangements for {springs} and {config}")
    #     total_arrangements += arrangements
print(f"The number of possible arrangements is: {total_arrangements}")
