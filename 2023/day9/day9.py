import functools


lines = []
with open("day9.txt") as file:
    lines = [l.strip().split(" ") for l in file.readlines() if l.strip()]

line = "0 3 6 9 12 15".split(" ")


def next_line(line):
    return [int(line[a + 1]) - int(line[a]) for a in range(len(line) - 1)]


def predict(line):
    if not any(line):
        return 0
    return int(line[-1]) + predict(next_line(line))


def predict_back(line):
    if not any(line):
        return 0
    return int(line[0]) - predict_back(next_line(line))


print(functools.reduce(lambda a, b: a + b, map(predict, lines)))
print(functools.reduce(lambda a, b: a + b, map(predict_back, lines)))
