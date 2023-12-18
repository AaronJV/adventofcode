from collections import namedtuple
from queue import PriorityQueue
import sys
from aoc import AdventOfCode

Node = namedtuple("Node", ["pos", "dir", "dir_count"])

DOWN = (1, 0)
UP = (-1, 0)
RIGHT = (0, 1)
LEFT = (0, -1)


class Day17Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 17, use_example=use_example)

    def get_next_nodes(self, current_node, min, max):
        i, j = current_node.pos
        next_nodes = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            di, dj = direction
            new_pos = (i + di, j + dj)
            if (
                new_pos[0] < 0
                or new_pos[0] > len(self.data) - 1
                or new_pos[1] < 0
                or new_pos[1] > len(self.data[0]) - 1
            ):
                continue
            dir_count = (
                current_node.dir_count + 1 if current_node.dir == direction else 1
            )
            if dir_count > max:
                continue
            if current_node.dir != direction and current_node.dir_count < min:
                continue
            if current_node.dir == (direction[0] * -1, direction[1] * -1):
                continue
            next_nodes.append(Node(new_pos, direction, dir_count))
        return next_nodes

    def get_path(self, min, max):
        exploring = PriorityQueue()
        costs = dict()
        visited = set()

        exploring.put((0, Node((0, 0), (1, 0), 0)))
        exploring.put((0, Node((0, 0), (0, 1), 0)))
        while not exploring.empty():
            current_cost, node = exploring.get()

            if node in visited:
                continue
            visited.add(node)

            costs[node] = current_cost

            for next_node in self.get_next_nodes(node, min, max):
                if next_node in visited:
                    continue
                heat_loss = current_cost + self.data[next_node.pos[0]][next_node.pos[1]]

                if next_node not in costs or costs[node] > heat_loss:
                    exploring.put((heat_loss, next_node))

        min_val = sys.maxsize
        for node, cost in costs.items():
            if (
                node.pos[0] == len(self.data) - 1
                and node.pos[1] == len(self.data[0]) - 1
                and node.dir_count >= min
            ):
                if cost < min_val:
                    min_val = cost
        return min_val

    def parse_data(self, data):
        return [[int(c) for c in l.strip()] for l in data.split("\n") if l.strip()]

    def part_1(self):
        print("Minimum heat loss =", self.get_path(0, 3))

    def part_2(self):
        print("Minimum heat loss =", self.get_path(4, 10))


Day17Solution(use_example=False).solve()
