import time

lines = []
with open("day14.txt") as file:
    lines = [l.strip() for l in file.readlines() if l.strip()]


def part_1():
    value = 0

    def get_col(group, col):
        return "".join([line[col] for line in group if line[col] != "."])

    for j in range(len(lines[0])):
        rocks = get_col(lines, j)
        if len(rocks) == 0:
            print(j, rocks)
        for i in range(len(lines)):
            if lines[i][j] == "#" and rocks[0] == "#":
                rocks = rocks[1:]
            elif rocks[0] == "O":
                value += len(lines) - i
                rocks = rocks[1:]
            if len(rocks) == 0:
                break

    print("part1:", value)


def tilt_ns(dish, is_north):
    def get_col(group, col):
        return "".join([line[col] for line in group if line[col] != "."])

    # north
    start = 0 if is_north else len(dish) - 1
    end = -1 if not is_north else len(dish)
    step = 1 if is_north else -1
    for j in range(len(dish[0])):
        rocks = get_col(dish, j)
        if not is_north:
            rocks = rocks[::-1]
        if len(rocks) == 0:
            print(j, rocks)
        for i in range(start, end, step):
            if len(rocks) == 0:
                if dish[i][j] != "#":
                    dish[i][j] = "."
                continue
            if dish[i][j] == "#" and rocks[0] == "#":
                rocks = rocks[1:]
            elif rocks[0] == "O":
                rocks = rocks[1:]
                dish[i][j] = "O"
            else:
                dish[i][j] = "."


def tilt_ew(dish, is_west):
    def get_row(group, row):
        return "".join([rock for rock in group[row] if rock != "."])

    start = 0 if is_west else len(dish[0]) - 1
    end = -1 if not is_west else len(dish[0])
    step = 1 if is_west else -1
    # west
    for i in range(len(dish)):
        rocks = get_row(lines, i)
        if not is_west:
            rocks = rocks[::-1]
        if len(rocks) == 0:
            print(j, rocks)
        for j in range(start, end, step):
            if len(rocks) == 0:
                if lines[i][j] != "#":
                    dish[i][j] = "."
                continue
            if lines[i][j] == "#" and rocks[0] == "#":
                rocks = rocks[1:]
            elif rocks[0] == "O":
                rocks = rocks[1:]
                dish[i][j] = "O"
            else:
                dish[i][j] = "."


def tilt(dish):
    new = [[r for r in line] for line in dish]
    tilt_ns(new, True)
    tilt_ew(new, True)
    tilt_ns(new, False)
    tilt_ew(new, False)
    return new


def hash(dish):
    return "\n".join(["".join([r for r in line]) for line in dish])


def part_2():
    dish = [[c for c in line] for line in lines]
    seen = [hash(dish)]

    while True:
        dish = tilt(dish)
        h = hash(dish)
        if h in seen:
            print(len(seen))
            start = seen.index(h)
            break
        seen.append(h)

    value = 0

    print(((1000000000 - len(seen)) % (start - len(seen))) + len(seen) - 1)

    final_dish = seen[((1000000000 - len(seen)) % (start - len(seen))) + len(seen) - 1]

    for j in range(len(final_dish[0])):
        for i in range(len(final_dish)):
            if final_dish[i][j] == "O":
                value += len(final_dish) - i

    print("part2:", value)


start = time.perf_counter_ns()
part_1()
end = time.perf_counter_ns()
print(f"Part 1 tool {(end-start)/1000} ms")


start = time.perf_counter_ns()
part_2()
end = time.perf_counter_ns()
print(f"Part 2 tool {(end-start)/1000} ms")
