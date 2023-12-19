from aoc import AdventOfCode


class Day2Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 2, use_example=use_example)

    def parse_data(self, data):
        games = dict()
        for line in data.split("\n"):
            if not line:
                continue
            id, game = line.split(":")
            id = int(id.replace("Game ", ""))
            games[id] = {
                "blue": 0,
                "green": 0,
                "red": 0,
            }
            for g in game.split(";"):
                for cubes in g.split(","):
                    count, colour = cubes.strip().split(" ")
                    if games[id][colour] < int(count):
                        games[id][colour] = int(count)
        return games

    def part_1(self):
        BLUE = 14
        RED = 12
        GREEN = 13
        sum = 0
        for id, game in self.data.items():
            if game["red"] > RED or game["blue"] > BLUE or game["green"] > GREEN:
                continue
            sum += id
        print(sum)

    def part_2(self):
        sum = 0
        for game in self.data.values():
            sum += game["red"] * game["blue"] * game["green"]
        print(sum)


Day2Solution(use_example=False).solve()
