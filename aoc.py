import argparse
import datetime
from html.parser import HTMLParser
import os
import time
import requests


class ExampleParser(HTMLParser):
    in_pre = False
    found = False
    reading = False
    data = None

    def handle_starttag(self, tag, attributes):
        if self.found:
            return
        if tag == "code" and self.in_pre:
            self.found = True
            self.reading = True
        if tag == "pre":
            self.in_pre = True

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
        if tag == "code" and self.reading:
            self.reading = False

    def handle_data(self, data):
        if self.reading:
            self.data = data


def get_sesession():
    session = os.getenv("AOC_SESSION")

    if session:
        return session

    env = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.isfile(env):
        with open(env) as file:
            for line in file.readlines():
                var, val = line.strip().split("=")
                os.environ[var] = val

    session = os.getenv("AOC_SESSION")

    if session:
        return session

    raise Exception("Could not retrieve AOC session")


def get_data(year, day, output_dir: str = None):
    path = f"input-{year}-{day}.txt"
    if output_dir:
        path = os.path.join(output_dir, path)
    if os.path.isfile(path):
        with open(path) as file:
            return file.read()

    session = get_sesession()

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(
        url,
        cookies={"session": session},
    )
    if response.status_code >= 400:
        if response.status_code == 404:
            raise Exception(f"{year}/{day} not available yet")
        print("got %s status code token=%s", response.status_code)
        print(response.text)
        raise Exception(f"HTTP {response.status} at {url}")
    with open(path, "w") as f:
        f.write(response.text)

    return response.text


def get_example(year, day):
    path = f"input-{year}-{day}-sample.txt"
    if os.path.isfile(path):
        with open(path) as file:
            return file.read()

    url = f"https://adventofcode.com/{year}/day/{day}"

    session = get_sesession()

    response = requests.get(
        url,
        cookies={"session": session},
    )

    if response.status_code >= 400:
        if response.status_code == 404:
            raise Exception(f"{year}/{day} not available yet")
        print("got %s status code token=%s", response.status_code)
        print(response.text)
        raise Exception(f"HTTP {response.status} at {url}")
    parser = ExampleParser()
    parser.feed(response.text)
    with open(path, "w") as f:
        f.write(parser.data)
        return parser.data


class AdventOfCode:
    def __init__(self, year, day, use_example=False) -> None:
        if datetime.date.today() < datetime.date(year, 12, day):
            raise Exception("too early")
        data = get_data(year, day)
        self.use_example = use_example
        if use_example:
            data = get_example(year, day)

        print("\nParsing Input")
        start = time.time()
        self.data = self.parse_data(data)
        duration = time.time() - start
        print(f"Parsing Input took {duration} seconds\n")

    def parse_data(self, data):
        return [line for line in data.split("\n") if line.strip()]

    def solve(self):
        print("Running Part 1" + (" using example input" if self.use_example else ""))
        start = time.time()
        self.part_1()
        duration = time.time() - start
        print(f"Part 1 took {duration} seconds")

        print("\nRunning Part 2" + (" using example input" if self.use_example else ""))
        start = time.time()
        self.part_2()
        duration = time.time() - start
        print(f"Part 2 took {duration} seconds")

    def part_1(self):
        print("Part 1")

    def part_2(self):
        print("Part 2")


template = """from aoc import AdventOfCode

class Day<DAY>Solution(AdventOfCode):
    def __init__(self, use_example) -> None:
        super().__init__(<YEAR>, <DAY>, use_example=use_example)

    def part_1(self):
        print("Part 1")

    def part_2(self):
        print("Part 2")

Day<DAY>Solution(use_example=True).solve()
"""

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser("AOC library")
    arg_parser.add_argument("-g", "--generate", action="store_true", default=False)
    arg_parser.add_argument("-d", "--day", required=True)
    arg_parser.add_argument("-y", "--year", required=True)

    parsed = arg_parser.parse_args()
    if parsed.generate:
        path = os.path.join(parsed.year, f"day{parsed.day}", f"day{parsed.day}.py")
        if os.path.exists(path):
            print(f"{path} exists")
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(
                    template.replace("<DAY>", parsed.day).replace("<YEAR>", parsed.year)
                )
            if datetime.date.today() >= datetime.date(
                int(parsed.year), 12, int(parsed.day)
            ):
                get_data(parsed.year, parsed.day, output_dir=os.path.dirname(path))
    else:
        print(parsed)
