from collections import namedtuple
from math import lcm
from aoc import AdventOfCode


HIGH = True
LOW = False


class Module:
    def __init__(self, name, mod_type, outputs) -> None:
        self.name = name
        self.mod_type = mod_type
        self.outputs = outputs
        self.state = False

    def pulse(self, pulse, source):
        if self.mod_type == "&":
            self.inputs[source] = pulse
            return [
                (label, not all(self.inputs.values()), self.name)
                for label in self.outputs
            ]
        if self.mod_type == "%":
            if pulse == LOW:
                self.state = not self.state
                return [(label, self.state, self.name) for label in self.outputs]
            return []
        return [(label, pulse, self.name) for label in self.outputs]

    def set_intputs(self, inputs):
        if self.mod_type != "&":
            return

        self.inputs = {input: False for input in inputs}

    def reset(self):
        self.state = False
        if self.mod_type == "&":
            self.inputs = {input: False for input in self.inputs.keys()}


class Day20Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(2023, 20, use_example=use_example)

    def parse_data(self, data):
        modules = dict()
        cons = []
        for line in data.split("\n"):
            if not line:
                continue
            label, outputs = line.split(" -> ")
            button_type = ""
            if label[0] == "%" or label[0] == "&":
                button_type = label[0]
                label = label[1:]
            mod = Module(label, button_type, outputs.split(", "))
            if mod.mod_type == "&":
                cons.append(mod)
            modules[label] = mod
        for con in cons:
            inputs = [mod.name for mod in modules.values() if con.name in mod.outputs]
            con.set_intputs(inputs)
        return modules

    def part_1(self):
        low_count = 0
        high_count = 0
        for _ in range(1000):
            mod_queue = [("broadcaster", LOW, "")]
            low_count += 1

            while len(mod_queue):
                module, pulse, source = mod_queue.pop(0)

                if module in self.data:
                    next_mods = self.data[module].pulse(pulse, source)
                    for mod, p, s in next_mods:
                        if p:
                            high_count += 1
                        else:
                            low_count += 1
                    mod_queue.extend(next_mods)

        print("Part 1", low_count * high_count)

    def part_2(self):
        for mod in self.data.values():
            mod.reset()
        presses = 0
        rx_source = next(
            (mod.name for mod in self.data.values() if "rx" in mod.outputs)
        )
        rx_source_presses = {}
        rx_source_count = len(
            [mod for mod in self.data.values() if rx_source in mod.outputs]
        )

        while len(rx_source_presses) < rx_source_count:
            mod_queue = [("broadcaster", LOW, "")]
            presses += 1

            while len(mod_queue):
                module, pulse, source = mod_queue.pop(0)

                if module == rx_source and pulse:
                    rx_source_presses[source] = presses

                if module in self.data:
                    next_mods = self.data[module].pulse(pulse, source)
                    mod_queue.extend(next_mods)
        print("Part 2:", lcm(*rx_source_presses.values()))


Day20Solution(use_example=False).solve()
