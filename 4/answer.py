DAY = 4
USE_EXAMPLE = True

with open(f"{DAY}/example.txt" if USE_EXAMPLE else f"{DAY}/input.txt", encoding="utf-8") as f:
    lines = f.readlines()

answer = 0
for line in lines:
    card_info, number_info = line.split(":")
    card = card_info.split()[1]
    numbers = number_info.split("|")
    winning_numbers = {int(n) for n in numbers[0].split()}
    numbers = {int(n) for n in numbers[1].split()}
    wins = numbers & winning_numbers
    points = 0
    if wins:
        points += pow(2, len(wins) - 1)
        print(
            f"Card {card} has {len(wins)} winning numbers ({", ".join(str(w) for w in wins)}), so it is worth {points} points."
        )
    else:
        print(f"Card {card} has no winning numbers, so it is worth no points.")
    answer += points
print(f"The Elf's pile of scratchcards is worth {answer} points.")
