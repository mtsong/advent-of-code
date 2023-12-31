DAY = 4
USE_EXAMPLE = False

with open(f"{DAY}/example.txt" if USE_EXAMPLE else f"{DAY}/input.txt", encoding="utf-8") as f:
    lines = f.readlines()

answer = 0
cards = []
for line in lines:
    card_info, number_info = line.split(":")
    card_num = card_info.split()[1]
    numbers = number_info.split("|")
    winning_numbers = {int(n) for n in numbers[0].split()}
    numbers = {int(n) for n in numbers[1].split()}
    cards.append((card_num, winning_numbers, numbers))

winning_copies = []


def copy_winning_cards(card):
    card_num, winning_numbers, numbers = card
    wins = numbers & winning_numbers
    if len(wins) == 0:
        return
    copies = cards[int(card_num) : int(card_num) + len(wins)]
    winning_copies.extend(copies)
    for copy in copies:
        copy_winning_cards(copy)


for card in cards:
    copy_winning_cards(card)

winning_cards = cards + winning_copies
print(f"The Elf's ends up with {len(winning_cards)} cards.")
