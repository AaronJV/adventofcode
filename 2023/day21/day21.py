from aoc import AdventOfCode


class Day21Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 21, use_example=use_example)

    def start_pos(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == "S":
                    return (i, j)

    def step(self, locations):
        new_locations = set()

        for location in locations:
            (i, j) = location
            for delta in range(-1, 2, 2):
                if (
                    i + delta >= 0
                    and (i + delta) < len(self.data)
                    and self.data[i + delta][j] != "#"
                ):
                    new_locations.add((i + delta, j))
                if (
                    j + delta >= 0
                    and (j + delta) < len(self.data)
                    and self.data[i][j + delta] != "#"
                ):
                    new_locations.add((i, j + delta))

        return new_locations

    def print_grid(self, locations):
        count = 0
        for i, line in enumerate(self.data):
            for j, c in enumerate(line):
                if (i, j) in locations:
                    print("O", end="")
                    count += 1
                else:
                    print(c, end="")
            print()

    def part_1(self):
        locations = {self.start_pos()}

        for _ in range(64):
            locations = self.step(locations)

        print("Part 1", len(locations))

    def get_grid_step_count(self, start_i, start_j, steps, debug=False):
        locations = {(start_i, start_j)}
        for _ in range(steps):
            locations = self.step(locations)
        if debug:
            self.print_grid(locations)
        return len(locations)

    def part_2(self):
        # input data has start col and row clear, so path will expand out in diamond pattern,
        # with full grids making checker board pattern of odd and even parity
        # looking at the step goal and the size of the grid, the tips of the paths will be the
        # very edge and the edges will repeat a large and small fill pattern
        # e.g. leftmost garden and
        # ---+---
        # ./#|###
        # <##|###
        # .\#|###
        # ---+---
        # ..\|###
        # ...|\##
        # ...|.\#
        step_goal = 26501365
        size = self.width

        garden_size = int(step_goal / size) - 1
        partial_steps_small = int(size / 2) - 1
        partial_steps_big = int(3 * size / 2) - 1

        top_left_small = self.get_grid_step_count(
            size - 1, size - 1, partial_steps_small
        )
        top_right_small = self.get_grid_step_count(size - 1, 0, partial_steps_small)
        bottom_left_small = self.get_grid_step_count(0, size - 1, partial_steps_small)
        bottom_right_small = self.get_grid_step_count(0, 0, partial_steps_small)

        top_left_big = self.get_grid_step_count(size - 1, size - 1, partial_steps_big)
        top_right_big = self.get_grid_step_count(size - 1, 0, partial_steps_big)
        bottom_left_big = self.get_grid_step_count(0, size - 1, partial_steps_big)
        bottom_right_big = self.get_grid_step_count(0, 0, partial_steps_big)

        left = self.get_grid_step_count(int(size / 2), size - 1, size - 1)
        right = self.get_grid_step_count(int(size / 2), 0, size - 1)
        top = self.get_grid_step_count(size - 1, int(size / 2), size - 1)
        bottom = self.get_grid_step_count(0, int(size / 2), size - 1)

        locations = {self.start_pos()}
        for _ in range(self.width * 2):
            locations = self.step(locations)
        even = len(locations)
        locations = self.step(locations)
        odd = len(locations)

        num_even = garden_size * garden_size + 2 * garden_size + 1
        num_odd = num_even - 2 * garden_size - 1

        pos_count = (
            (garden_size + 1)
            * (
                top_left_small
                + top_right_small
                + bottom_left_small
                + bottom_right_small
            )
            + garden_size
            * (top_left_big + top_right_big + bottom_left_big + bottom_right_big)
            + num_even * even
            + num_odd * odd
            + left
            + right
            + bottom
            + top
        )
        print("Part 2:", pos_count)


Day21Solution(use_example=False).solve()
