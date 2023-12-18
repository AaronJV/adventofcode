import time

lines = []
with open("day16.txt") as file:
    lines = [l.strip() for l in file.readlines() if l.strip()]


def print_grid(grid):
    count = 0
    for row in grid:
        for cell in row:
            if cell:
                print("#", end="")
                count += 1
            else:
                print(".", end="")
        print()
    print()
    return count


def do_lasers(start, debug=False):
    energized = [["" for i in lines[0]] for j in lines]
    beams = [start]
    while len(beams):
        done = []
        split = []
        for i, beam in enumerate(beams):
            pos = beam[0]
            if (
                pos[0] < 0
                or pos[0] >= len(lines)
                or pos[1] < 0
                or pos[1] >= len(lines[0])
            ):
                done.append(i)
                continue

            if lines[pos[0]][pos[1]] == "\\":
                beam[1] = [beam[1][1], beam[1][0]]
                energized[pos[0]][pos[1]] = "#"
            elif lines[pos[0]][pos[1]] == "/":
                beam[1] = [-1 * beam[1][1], -1 * beam[1][0]]
                energized[pos[0]][pos[1]] = "#"
            elif lines[pos[0]][pos[1]] == "|" and beam[1][1] != 0:
                done.append(i)
                if "#" in energized[pos[0]][pos[1]]:
                    continue
                split.append([[pos[0] + 1, pos[1]], [1, 0]])
                split.append([[pos[0] - 1, pos[1]], [-1, 0]])
                energized[pos[0]][pos[1]] += "#"
                continue
            elif lines[pos[0]][pos[1]] == "-" and beam[1][0] != 0:
                done.append(i)
                if "#" in energized[pos[0]][pos[1]]:
                    continue
                split.append([[pos[0], pos[1] + 1], [0, 1]])
                split.append([[pos[0], pos[1] - 1], [0, -1]])
                energized[pos[0]][pos[1]] += "#"
                continue

            if beam[1][0] != 0 and "|" in energized[pos[0]][pos[1]]:
                done.append(i)
                continue

            if beam[1][1] != 0 and "-" in energized[pos[0]][pos[1]]:
                done.append(i)
                continue
            if "#" not in energized[pos[0]][pos[1]]:
                energized[pos[0]][pos[1]] += "-" if beam[1][1] else "|"
            beam[0][0] += beam[1][0]
            beam[0][1] += beam[1][1]
        for i in reversed(done):
            beams.pop(i)
        beams.extend(split)

    count = 0
    for row in energized:
        for cell in row:
            if cell:
                count += 1
    if debug:
        print_grid(energized)
    return count


def part_1():
    count = do_lasers([[0, 0], [0, 1]])
    print("Part 1", count)


def part_2():
    starts = []

    for i in range(len(lines)):
        starts.append([[0, i], [1, 0]])
        starts.append([[len(lines[0]) - 1, i], [-1, 0]])
    for i in range(len(lines[0])):
        starts.append([[i, 0], [0, 1]])
        starts.append([[i, len(lines) - 1], [0, -1]])
    count = max([do_lasers(s) for s in starts])
    print("Part 2", count)


start = time.perf_counter_ns()
part_1()
end = time.perf_counter_ns()
print(f"Part 1 tool {(end-start)/1000} ms")


start = time.perf_counter_ns()
part_2()
end = time.perf_counter_ns()
print(f"Part 2 tool {(end-start)/1000} ms")
