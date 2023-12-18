import time

lines = []
with open("day13.txt") as file:
    lines = [l.strip() for l in file.readlines()]


def reflections(group, smudges=0):
    horizontal = 0
    vertical = 0

    for i in range(1, len(group)):
        diff_chars = 0
        steps = min(i, len(group) - i)
        for i_0 in range(0, steps):
            diff_chars += sum(
                1 for a, b in zip(group[i + i_0], group[i - i_0 - 1]) if a != b
            )
            if diff_chars > smudges:
                break
        if diff_chars == smudges:
            horizontal = i
            break

    def get_col(group, col):
        return "".join([line[col] for line in group])

    for j in range(1, len(group[0])):
        diff_chars = 0
        steps = min(j, len(group[0]) - j)
        for j_0 in range(0, steps):
            diff_chars += sum(
                1
                for a, b in zip(get_col(group, j + j_0), get_col(group, j - j_0 - 1))
                if a != b
            )
            if diff_chars > smudges:
                break
        if diff_chars == smudges:
            vertical = j
            break

    return vertical + 100 * horizontal


def part_1():
    groups = []
    curr = []
    for line in lines:
        if not line:
            groups.append(curr)
            curr = []
        else:
            curr.append(line)
    if len(curr):
        groups.append(curr)
    print(len(groups))
    value = sum([reflections(group) for group in groups])
    print("part1:", value)


def part_2():
    groups = []
    curr = []
    for line in lines:
        if not line:
            groups.append(curr)
            curr = []
        else:
            curr.append(line)
    if len(curr):
        groups.append(curr)
    print(len(groups))
    value = sum([reflections(group, 1) for group in groups])
    print("part2:", value)


start = time.perf_counter_ns()
part_1()
end = time.perf_counter_ns()
print(f"Part 1 tool {(end-start)/1000} ms")


start = time.perf_counter_ns()
part_2()
end = time.perf_counter_ns()
print(f"Part 2 tool {(end-start)/1000} ms")
