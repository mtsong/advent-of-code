import pathlib
from enum import Enum
from collections import Counter

USE_EXAMPLE = False
CWD = pathlib.Path(__file__).parent.resolve()
hands = []
with open(CWD / ("example.txt" if USE_EXAMPLE else "input.txt"), encoding="utf-8") as f:
    for line in f:
        hand, bid = line.split()
        hands.append((hand, int(bid)))


CARDS = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Hand(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def get_hand(hand: tuple[str, int]) -> Hand:
    unique_cards = set(hand[0])
    counter = Counter(hand[0])
    sets = counter.most_common()
    # Convert jokers to biggest set
    jokers = 0
    if "J" in unique_cards:
        jokers = counter["J"]
        unique_cards.remove("J")
        counter.pop("J")
        sets = counter.most_common()
    if not unique_cards or len(unique_cards) == 1:  # Five of a kind
        return Hand.FIVE_OF_A_KIND.value
    for _, num in sets:
        num += jokers
        if num == 4:  # Four of a kind
            return Hand.FOUR_OF_A_KIND.value
        if num == 3:
            if len(unique_cards) == 2:
                return Hand.FULL_HOUSE.value
            return Hand.THREE_OF_A_KIND.value
        if num == 2:
            if len(unique_cards) == 3:
                return Hand.TWO_PAIR.value
            return Hand.ONE_PAIR.value
    return Hand.HIGH_CARD.value


# First sort by card order, then by hand rank
hands.sort(key=lambda h: [CARDS[c] for c in h[0]])
hands.sort(key=get_hand)
answer = 0
for i, hand in enumerate(hands):
    answer += (i + 1) * hand[1]
print(f"The total winnings are {answer}")
