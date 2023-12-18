with open("day3.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]


def is_part_number(i, j, num_len):
    max_x = len(lines)
    max_y = len(lines[i])
    valid = False
    gears = []
    for x in range(i - 1, i + 2):
        for y in range(j - num_len - 1, j + 1):
            if (
                0 < x < max_x
                and 0 < y < max_y
                and lines[x][y] != "."
                and not lines[x][y].isdigit()
            ):
                valid = True
                if lines[x][y] == "*":
                    gears.append(f"{x},{y}")
    return valid, gears


sum = 0
all_gears = dict()
ratios = dict()
for i, line in enumerate(lines):
    j = 0
    num_start = 0
    number = ""
    for j, value in enumerate(line):
        if value.isdigit():
            number += value
        else:
            if number:
                valid, gears = is_part_number(i, j, len(number))
                if valid:
                    # check around number
                    sum += int(number)
                    for gear in gears:
                        if gear in all_gears:
                            all_gears[gear] = all_gears[gear] + 1
                            ratios[gear] = ratios[gear] * int(number)
                        else:
                            all_gears[gear] = 1
                            ratios[gear] = int(number)
            number = ""
            num_start = j
    if number:
        valid, gears = is_part_number(i, j, len(number))
        if valid:
            # check around number
            sum += int(number)
            for gear in gears:
                if gear in all_gears:
                    all_gears[gear] = all_gears[gear] + 1
                    ratios[gear] = ratios[gear] * int(number)
                else:
                    all_gears[gear] = 1
                    ratios[gear] = int(number)
    number = ""
    num_start = j

print(sum)
ratio_sum = 0
for gear, count in all_gears.items():
    if count > 1:
        ratio_sum += ratios[gear]
print(ratio_sum)
