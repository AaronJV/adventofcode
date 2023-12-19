from collections import namedtuple
import copy
import time
from aoc import AdventOfCode

Rule = namedtuple("Rule", ["key", "cmp", "value", "dest"])


class Day19Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 19, use_example=use_example)

    def parse_data(self, data):
        at_parts = False
        workflows = dict()
        parts = []
        for line in data.split("\n"):
            if not line:
                at_parts = True
                continue
            if at_parts:
                part = {
                    l.split("=")[0]: int(l.split("=")[1]) for l in line[1:-1].split(",")
                }
                parts.append(part)
            else:
                name, rules = line.split("{")
                rules = rules.strip("}").split(",")
                workflows[name] = [self.parse_rule(rule) for rule in rules]
        workflows["A"] = [Rule(None, None, None, "A")]
        workflows["R"] = [Rule(None, None, None, "R")]
        self.parts = parts
        self.workflows = workflows
        return data

    def parse_rule(self, rule):
        if ":" not in rule:
            return Rule(key=None, cmp=None, value=None, dest=rule)
        condition, dest = rule.split(":")
        return Rule(
            key=condition[0:1], dest=dest, cmp=condition[1:2], value=int(condition[2:])
        )

    def next_workflow(self, workflow, part, debug=False):
        if workflow not in self.workflows:
            return "R"
        rules = self.workflows[workflow]
        for rule in rules:
            if debug:
                print(workflow, rule, part)
            if rule.key is None:
                return rule.dest
            val = part[rule.key]
            if rule.cmp == "<" and val < rule.value:
                return rule.dest
            if rule.cmp == ">" and val > rule.value:
                return rule.dest
        return "R"

    def sort_part(self, part, debug=False):
        workflow = "in"

        while workflow != "A" and workflow != "R":
            workflow = self.next_workflow(workflow, part, debug=debug)
            if debug:
                print(workflow)
        return workflow

    def part_1(self):
        sum = 0
        for part in self.parts:
            if self.sort_part(part) == "A":
                sum += part["x"] + part["m"] + part["a"] + part["s"]
        print("Part 1:", sum)

    def part_2(self):
        ranges = []
        exploring = [
            (
                {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]},
                self.workflows["in"],
            )
        ]
        while len(exploring):
            prod_range, workflow = exploring.pop(0)
            for rule in workflow:
                if rule.key is None:
                    if rule.dest == "A":
                        ranges.append(copy.deepcopy(prod_range))
                    elif rule.dest != "R":
                        exploring.append(
                            (copy.deepcopy(prod_range), self.workflows[rule.dest])
                        )
                elif rule.cmp == "<":
                    nested_range = copy.deepcopy(prod_range)
                    nested_range[rule.key][1] = rule.value - 1
                    prod_range[rule.key][0] = rule.value
                    exploring.append((nested_range, self.workflows[rule.dest]))
                elif rule.cmp == ">":
                    nested_range = copy.deepcopy(prod_range)
                    nested_range[rule.key][0] = rule.value + 1
                    prod_range[rule.key][1] = rule.value
                    exploring.append((nested_range, self.workflows[rule.dest]))

        sum = 0
        for prod_range in ranges:
            product = 1
            for part_range in prod_range.values():
                product *= part_range[1] - part_range[0] + 1
            sum += product

        print("Part 2", sum)


Day19Solution(use_example=False).solve()
