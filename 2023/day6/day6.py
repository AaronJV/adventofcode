import math


race1 = [47, 400]
race2 = [98, 1213]
race3 = [66, 1011]
race4 = [98, 1540]


def ways_to_win(race):
    count = 0
    for i in range(race[0]):
        if (race[0] - i) * i > race[1]:
            count = count + 1
    return count


print(ways_to_win(race1), race1)
print(ways_to_win(race2), race2)
print(ways_to_win(race3), race3)
print(ways_to_win(race4), race4)
print(
    "Part 1:",
    ways_to_win(race1) * ways_to_win(race2) * ways_to_win(race3) * ways_to_win(race4),
)

part2_t = 47986698
part2_d = 400121310111540


def get_min_time(low, high):
    mid = int((high + low) / 2)
    if high == mid + 1:
        return mid
    if ((part2_t - mid) * mid) > part2_d:
        return get_min_time(low, mid)
    elif ((part2_t - mid) * mid) < part2_d:
        return get_min_time(mid, high)
    return mid


def get_max_time(low, high):
    mid = int((high + low) / 2)
    if high == mid + 1:
        return mid
    if ((part2_t - mid) * mid) < part2_d:
        return get_max_time(low, mid)
    elif (part2_t - mid) * mid > part2_d:
        return get_max_time(mid, high)
    return mid


min = get_min_time(0, part2_t)
max = get_max_time(0, part2_t)
print("Part 2:", max - min)


def calc_game(time, distance):
    return math.floor(math.sqrt(time**2 - 4 * distance))


print(
    "Part 1:",
    calc_game(*race1) * calc_game(*race2) * calc_game(*race3) * calc_game(*race4),
)
print("Part 1:", calc_game(part2_t, part2_d))
