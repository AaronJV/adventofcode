import functools

lines = []
with open("day5.txt") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines if line.rstrip()]

seed_lines = ""
maps = [dict()]

for line in lines[2:]:
    if line.endswith("map:"):
        maps.append(dict())
        continue
    else:
        dest_range, source_range, length = line.split(" ")
        maps[len(maps) - 1][int(source_range)] = [int(dest_range), int(length)]

seeds = [int(seed) for seed in lines[0].replace("seeds:", "").split(" ") if seed]


def mapper(map, value):
    return next(
        (
            int(map[val][0]) + (value - int(val))
            for val in map.keys()
            if int(val) <= value and int(val) + int(map[val][1]) >= value
        ),
        value,
    )


def map_seed(seed):
    return functools.reduce(lambda value, map: mapper(map, value), maps, seed)


locations = []
for seed in seeds:
    locations.append(map_seed(seed))

print("Part 1:", min(locations))

part2_location = 0


def make_range(list):
    it = iter(list)
    return zip(it, it)


def reverse_map(map, value):
    for source_start, dest_range in map.items():
        if dest_range[0] <= value and value <= dest_range[0] + dest_range[1]:
            return source_start + (value - dest_range[0])
    return value


def location_has_seed(location, seed_ranges):
    seed = functools.reduce(
        lambda value, map: reverse_map(map, value), reversed(maps), location
    )

    for start, length in seed_ranges:
        if seed >= start and seed <= start + length:
            return True
    return False


seed_ranges = [seed_range for seed_range in make_range(seeds)]
found_seed = False
while not found_seed:
    if location_has_seed(part2_location, seed_ranges):
        found_seed = True
    else:
        part2_location += 1

print("Part 2:", part2_location)
