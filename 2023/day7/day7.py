import functools

lines = []
with open("day7.txt") as file:
    lines = file.readlines()


def get_rank(a, use_jokers):
    counts = {}
    for char in a:
        counts[char] = (counts[char] + 1) if char in counts else 1
    jokers = 0
    if use_jokers and "J" in counts:
        jokers = counts["J"]
        if jokers == 5:
            return 0
        del counts["J"]

    max_count = max(counts.values()) + jokers
    if max_count == 5:
        return 0
    if max_count == 4:
        return 1
    if max_count == 3 and len(counts) == 2:
        return 2
    if max_count == 3:
        return 3
    if max_count == 2 and len(counts) == 3:
        return 4
    if max_count == 2:
        return 5
    return 6


def parse_hand(line, use_jokers):
    hand, bid = line.rstrip().split(" ")
    rank = get_rank(hand, use_jokers)
    return [hand, rank, int(bid)]


cards = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}


def compare_hand(hand1, hand2, use_jokers):
    for i in range(5):
        c1 = hand1[i] if not use_jokers or hand1[i] != "J" else "0"
        c2 = hand2[i] if not use_jokers or hand2[i] != "J" else "0"
        c1 = int(c1) if c1.isdigit() else cards[c1]
        c2 = int(c2) if c2.isdigit() else cards[c2]

        if c1 > c2:
            return 1
        if c2 > c1:
            return -1
    return 0


def compare(item1, item2, use_jokers):
    if item1[1] == item2[1]:
        return compare_hand(item1[0], item2[0], use_jokers)
    if item1[1] > item2[1]:
        return -1
    return 1


def calc_winnings(use_jokers):
    hands = [parse_hand(line, use_jokers) for line in lines if line.rstrip()]
    # Calling
    hands.sort(key=functools.cmp_to_key(lambda x, y: compare(x, y, use_jokers)))

    winnings = 0
    for i in range(len(hands)):
        winnings += (i + 1) * hands[i][2]
    return winnings


print("Part 1:", calc_winnings(False))
print("Part 2:", calc_winnings(True))
