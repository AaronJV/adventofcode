import functools


lines = []
with open("day12.txt") as file:
    lines = [l.strip().split(" ") for l in file.readlines() if l.strip()]


def check_pattern(pattern, groups):
    if not len(groups):
        return 0
    if len(pattern) <= sum(groups):
        return 0
    group = groups.pop(0)
    patterns = []
    pattern_counts = 0
    for pattern_start in range(len(pattern) - group + 1):
        start_pos = max(pattern_start - 1, 0)
        start = pattern[start_pos]
        end_pos = pattern_start + group
        end = pattern[end_pos] if len(pattern) > end_pos else end_pos - 1
        if pattern_start == 0:
            start = "."
        if end_pos == len(pattern):
            end = "."
        if start == "#" or end == "#":
            continue
        segment = pattern[start_pos:end_pos]
        if "." in segment:
            continue
        if not len(groups):
            patterns.append((pattern_start, end_pos))
            pattern_counts += 1
        else:
            new_pattern = pattern[0:start_pos] + pattern[end_pos + 1 :]
            print(pattern, new_pattern, start_pos, end_pos)
            nested = check_pattern(new_pattern, [*groups])
            for pos in nested:
                patterns.append([(pattern_start, end_pos), *nested])
    return patterns


def get_arrangements(line):
    pattern, groups = line
    sorted_groups = sorted([int(size) for size in groups.split(",")], reverse=True)
    if len(pattern) <= sum(sorted_groups):
        return 0

    for arrangements in check_pattern(pattern, sorted_groups):
        print(arrangements)


def gen_options(size, splits):
    @functools.cache
    def gen(rem_len, rem_splits):
        if len(rem_splits) == 0:
            yield "." * rem_len
            return

        a = rem_splits[0]
        rest = rem_splits[1:]
        after = sum(rest) + len(rest)

        for before in range(rem_len - after - a + 1):
            cand = "." * before + "#" * a + "."
            for opt in gen(rem_len - a - before - 1, rest):
                yield cand + opt

    return list(gen(size, splits))


def find_matches(pattern, splits):
    options = gen_options(len(pattern), tuple([int(g) for g in splits.split(",")]))

    for o in options:
        if all((c0 == c1 or c0 == "?") for c0, c1 in zip(pattern, o)):
            yield o


def find_matches_2(pattern, splits):
    pattern = "?".join([pattern, pattern, pattern, pattern, pattern])
    options = gen_options(
        len(pattern), tuple([int(g) for g in (splits * 5).split(",")])
    )

    for o in options:
        if all((c0 == c1 or c0 == "?") for c0, c1 in zip(pattern, o)):
            yield o
