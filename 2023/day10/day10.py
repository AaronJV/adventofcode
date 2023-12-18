import os

os.system("color")

lines = []

with open("day10.txt") as file:
    lines = [l.strip() for l in file.readlines() if l.strip()]

maze = []
start = None

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

for i, line in enumerate(lines):
    maze.append(["▒" for _ in range(3 * len(line))])
    maze.append(["▒" for _ in range(3 * len(line))])
    maze.append(["▒" for _ in range(3 * len(line))])
    if "S" in line:
        start = [i, line.index("S")]
maze[3 * start[0] + 1][3 * start[1] + 1] = "S"


def get_next_dir(last, char):
    if last == UP:
        if char == "|":
            return UP
        if char == "7":
            return LEFT
        return RIGHT
    if last == DOWN:
        if char == "|":
            return DOWN
        if char == "J":
            return LEFT
        return RIGHT
    if last == LEFT:
        if char == "-":
            return LEFT
        if char == "F":
            return DOWN
        return UP
    if last == RIGHT:
        if char == "-":
            return RIGHT
        if char == "J":
            return UP
        return DOWN


def fill(maze):
    spread = [[0, 0]]

    while len(spread):
        x, y = spread.pop()
        maze[x][y] = " "
        if x > 0 and maze[x - 1][y] == "▒":
            spread.append([x - 1, y])
        if x < len(maze) - 1 and maze[x + 1][y] == "▒":
            spread.append([x + 1, y])
        if y > 0 and maze[x][y - 1] == "▒":
            spread.append([x, y - 1])
        if y < len(maze[0]) - 1 and maze[x][y + 1] == "▒":
            spread.append([x, y + 1])


char_map = {
    "|": ["▒█▒", "▒█▒", "▒█▒"],
    "-": ["▒▒▒", "███", "▒▒▒"],
    "F": ["▒▒▒", "▒██", "▒█▒"],
    "7": ["▒▒▒", "██▒", "▒█▒"],
    "L": ["▒█▒", "▒██", "▒▒▒"],
    "J": ["▒█▒", "██▒", "▒▒▒"],
    "S": ["███", "███", "███"],
}


def add_step(maze, char, x, y):
    for i in range(3):
        for j in range(3):
            try:
                maze[(3 * x) + i][(3 * y) + j] = char_map[char][i][j]
            except IndexError as e:
                print(len(maze), (3 * x) + i)
                print(len(maze[0]), (3 * y) + j)
                raise


def navigate(input_maze, new, start):
    count = 1
    dir = 0
    if start[0] > 0 and input_maze[start[0] - 1][start[1]] in "|7F":
        next = [start[0] - 1, start[1]]
        dir = get_next_dir(UP, input_maze[start[0] - 1][start[1]])
    elif start[0] < len(input_maze) - 1 and input_maze[start[0] + 1][start[1]] in "|JL":
        next = [start[0] - 1, start[1]]
        dir = get_next_dir(DOWN, input_maze[start[0] + 1][start[1]])
    elif start[1] > 0 and input_maze[start[0]][start[1] - 1] in "FL-":
        next = [start[0], start[1] - 1]
        dir = get_next_dir(LEFT, input_maze[start[0]][start[1] - 1])
    elif start[1] < len(input_maze[0]) and input_maze[start[0]][start[1] + 1] in "-J7":
        next = [start[0], start[1] - 1]
        dir = get_next_dir(RIGHT, input_maze[start[0]][start[1] + 1])

    add_step(new, input_maze[next[0]][next[1]], next[0], next[1])

    while input_maze[next[0]][next[1]] != "S":
        if dir == UP:
            next[0] = next[0] - 1
        if dir == DOWN:
            next[0] = next[0] + 1
        if dir == LEFT:
            next[1] = next[1] - 1
        if dir == RIGHT:
            next[1] = next[1] + 1
        dir = get_next_dir(dir, input_maze[next[0]][next[1]])
        add_step(new, input_maze[next[0]][next[1]], next[0], next[1])
        count += 1

    fill(maze)

    inner_count = 0
    for i in range(len(input_maze)):
        for j in range(len(input_maze[i])):
            if maze[3 * i + 1][3 * j + 1] == "▒":
                inner_count += 1
    return count, inner_count


length, inner_count = navigate(lines, maze, start)
print(length / 2)
print(inner_count)
for line in maze:
    print("".join(line))
