from collections import namedtuple
import sys
from aoc import AdventOfCode


Brick = namedtuple("Brick", ["x1", "y1", "z1", "x2", "y2", "z2", "id"])


def parse_coords(triplet):
    x, y, z = triplet.split(",")
    return (int(x), int(y), int(z))


class Day22Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 22, use_example=use_example)

    def parse_data(self, data):
        bricks = []
        for line in data.split("\n"):
            if not line.strip():
                continue
            start, end = line.split("~")
            bricks.append(
                Brick(*parse_coords(start), *parse_coords(end), len(bricks) + 1)
            )
        return bricks

    def settle(self):
        bricks = sorted(self.data, key=lambda b: b.z1)

        heights = dict()

        supported_by = dict()
        supports = dict()

        for brick in bricks:
            supported_by[brick.id] = set()
            supports[brick.id] = set()
            max_height = 0
            for x in range(brick.x1, brick.x2 + 1):
                for y in range(brick.y1, brick.y2 + 1):
                    height, id = heights.get((x, y), (1, None))
                    if height > max_height:
                        supported_by[brick.id].clear()
                        max_height = height

                    if height == max_height and id is not None:
                        supported_by[brick.id].add(id)

            for supporter in supported_by[brick.id]:
                supports[supporter].add(brick.id)

            height = brick.z2 - brick.z1 + 1
            for x in range(brick.x1, brick.x2 + 1):
                for y in range(brick.y1, brick.y2 + 1):
                    heights[(x, y)] = (max_height + height, brick.id)

        remove_candidates = set(range(len(bricks)))
        for supporter in supported_by.values():
            if len(supporter) == 1:
                remove_candidates.discard(supporter.pop())
        return bricks, supports, supported_by, remove_candidates

    def part_1(self):
        _, _, _, removable = self.settle()
        print("Part 1", len(removable))

    def part_2(self):
        bricks, supports, supported_by, _ = self.settle()
        sum = 0
        for brick in bricks:
            exploring = [brick.id]
            falling = set()

            falling_count = 0

            while len(exploring):
                explored = exploring.pop(0)
                for supported in supports[explored]:
                    if supported in falling:
                        continue
                    has_other_support = False
                    for may_fall in supported_by[supported]:
                        if may_fall not in falling:
                            has_other_support = True
                            break
                    if not has_other_support:
                        falling_count += 1
                        falling.add(supported)
                        exploring.append(supported)
            sum += falling_count
        print("Part 2", sum)


Day22Solution(use_example=False).solve()
