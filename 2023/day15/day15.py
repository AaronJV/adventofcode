import time

lines = []
with open("day15.txt") as file:
    lines = [l.strip() for l in file.readlines() if l.strip()]


def hash(text):
    val = 0
    for c in text:
        val += ord(c)
        val *= 17
        val = val % 256
    return val


def part_1():
    print("Part 1", sum([hash(line) for line in lines[0].split(",")]))


def part_2():
    boxes = [None] * 256
    steps = [step for step in lines[0].split(",")]
    for step in steps:
        operation = "=" if "=" in step else "-"
        label = step.split(operation)[0]
        box_num = hash(label)

        if boxes[box_num] is None:
            boxes[box_num] = []
        if operation == "-":
            if label in [lens[0] for lens in boxes[box_num]]:
                boxes[box_num].pop([lens[0] for lens in boxes[box_num]].index(label))
        else:
            if label in [lens[0] for lens in boxes[box_num]]:
                boxes[box_num][
                    [lens[0] for lens in boxes[box_num]].index(label)
                ] = step.split(operation)
            else:
                print(boxes[box_num])
                boxes[box_num].append(step.split(operation))
    value = 0
    for i, box in enumerate(boxes):
        if box is None:
            continue
        for j, lens in enumerate(box):
            value += (i + 1) * (j + 1) * int(lens[1])
    print(value)
    print("part 2")


start = time.perf_counter_ns()
part_1()
end = time.perf_counter_ns()
print(f"Part 1 tool {(end-start)/1000} ms")


start = time.perf_counter_ns()
part_2()
end = time.perf_counter_ns()
print(f"Part 2 tool {(end-start)/1000} ms")
