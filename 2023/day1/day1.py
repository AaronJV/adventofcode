from aoc import AdventOfCode

NUM_MAP = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7n",
    "eight": "e8t",
    "nine": "n9e",
    "zero": "0o",
}


def get_number(text: str):
    first = next((c for c in text if c.isdigit()))
    last = next((c for c in reversed(text) if c.isdigit()))
    return int(first + last)


def replace_number_words(text: str):
    for word, replacement in NUM_MAP.items():
        text = text.replace(word, replacement)
    return text


class Day1Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 1, use_example=use_example)

    def part_1(self):
        print("Part 1:", sum(map(get_number, self.data)))

    def part_2(self):
        print("Part 2:", sum(map(get_number, map(replace_number_words, self.data))))


Day1Solution(use_example=False).solve()
