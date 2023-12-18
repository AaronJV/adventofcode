from aoc import AdventOfCode


class Day18Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 18, use_example=use_example)

    def parse_data(self, data):
        return [l.split(" ") for l in data.split("\n") if l.strip()]

    def dig(self):
        """
        Initial attempt at part one - works for example input, but was having issues with
        actual input for the challenge
        - initially assumed that leftmost node == topmost node == (0,0) like in the example
        - changed to shoelace alg + counting the perimiter to get part one (making part 2 much easier)
        """
        pos = [0, 0]
        min_i = 0
        min_j = 0
        for line in self.data:
            direction = line[0]
            length = int(line[1])
            if direction == "R":
                pos[1] += length
            elif direction == "L":
                pos[1] -= length
            elif direction == "D":
                pos[0] += length
            elif direction == "U":
                pos[0] -= length

            if pos[1] < min_j:
                min_j = pos[1]
            if pos[0] < min_i:
                min_i = pos[0]

        if min_i < 0:
            pos[0] = (min_i * -1) + 2
        if min_j < 0:
            pos[1] = (min_j * -1) + 2

        print(pos)

        res = [["." for _ in range(pos[1] + 1)] for _ in range(pos[0] + 1)]
        res[pos[0]][pos[1]] = "#"
        try:
            for line in self.data:
                direction = line[0]
                length = int(line[1])

                if direction == "R":
                    while len(res[pos[0]]) <= pos[1] + length + 1:
                        res[pos[0]].append(".")
                    for i in range(length):
                        pos[1] += 1
                        res[pos[0]][pos[1]] = "#"

                if direction == "D":
                    while (len(res)) <= pos[0] + length:
                        res.append([])
                        for _ in range(pos[1]):
                            res[len(res) - 1].append(".")

                    for i in range(length):
                        pos[0] += 1
                        while len(res[pos[0]]) < pos[1] + 1:
                            res[pos[0]].append(".")
                        res[pos[0]][pos[1]] = "#"

                if direction == "L":
                    for i in range(length):
                        pos[1] -= 1
                        res[pos[0]][pos[1]] = "#"

                if direction == "U":
                    for i in range(length):
                        pos[0] -= 1
                        while len(res[pos[0]]) < pos[1] + 1:
                            res[pos[0]].append(".")
                        res[pos[0]][pos[1]] = "#"
        except:
            print(line)
        print(pos)
        count = 0
        print()

        for line in res:
            if "#" not in line:
                continue
            first = line.index("#")
            end = len(line) - line[::-1].index("#")
            count += end - first
            print("." * first, end="")
            print("#" * (end - first), end=" ")
            print(end - first)
        print(count)

    def shoe_lace(self, is_p2=False):
        i, j = 0, 0
        verts = [(0, 0)]

        perimeter = 0
        for line in self.get_data(is_p2):
            direction = line[0]
            length = int(line[1])
            perimeter += length
            if direction == "R":
                j += length
            elif direction == "L":
                j -= length
            elif direction == "D":
                i += length
            elif direction == "U":
                i -= length
            verts.append((i, j))

        sum_1 = 0
        for i in range(len(verts) - 1):
            sum_1 += (verts[i][0] + verts[i + 1][0]) * (verts[i + 1][1] - verts[i][1])

        # perimeter on top and left sides are included with the shoelace area (as top left is origin of cell)
        # so we need to halve the perimeter to get just the right and bottom cells
        # then add one for the right-most - bottom-most corner which won't be counted in the perimeter
        print(int(0.5 * abs(sum_1) + perimeter * 0.5 + 1))

    def get_data(self, is_p2):
        dirs = ["R", "D", "L", "U"]
        for line in self.data:
            if is_p2:
                yield dirs[int(line[2][7])], int(line[2][2:7], 16)
            else:
                yield line[0], int(line[1])

    def part_1(self):
        self.shoe_lace()

    def part_2(self):
        self.shoe_lace(True)
        print("Part 2")


Day18Solution(use_example=False).solve()
