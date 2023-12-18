import math

lines = []
with open("day8.txt") as file:
    lines = file.readlines()

instructions = lines[0]

mappping = dict()

for line in lines[2:]:
    place, dests = line.strip().split(" = ")
    mappping[place] = [dests[1:4], dests[6:9]]


def get_steps(place, end_only=False):
    steps = 0
    done = False
    while not done:
        index = 0 if instructions[steps % (len(instructions) - 1)] == "L" else 1
        place = mappping[place][index]
        steps += 1
        done = place == "ZZZ" if not end_only else place.endswith("Z")
    return steps


print(get_steps("AAA"))

places = [get_steps(p, True) for p in mappping if p.endswith("A")]
steps = math.lcm(*places)
print(steps)
