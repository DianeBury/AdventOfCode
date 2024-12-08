import functools

def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    return lines

def get_obstacles_per_line(lines: str):
    return [[i for i, char in enumerate(line) if char == '#'] for line in lines]

def get_obstacles_per_column(lines: str):
    obstacles_per_column = []
    for j in range(len(lines[0])):
        obstacles_per_column.append([i for i, line in enumerate(lines) if line[j]  == '#'])
    return obstacles_per_column

def is_guard(letter: str):
    if letter == "^":
        return True, (-1, 0)
    if letter == ">":
        return True, (0, 1)
    if letter == "<":
        return True, (0, -1)
    if letter == "v":
        return True, (1, 0)
    return False, None

def find_guard(lines: list[str]):
    for i, line in enumerate(lines):
        for j, letter in enumerate(line):
            res, direction = is_guard(letter)
            if res: return (i,j, direction)
    return None

def is_obstacle(lines, i, j, i_obstacle: int = -1, j_obstacle: int = -1):
    return lines[i][j] == "#" or (i == i_obstacle and j == j_obstacle)

def next_direction(direction):
    dx, dy = direction
    return (dy, -dx)

def walk_one(lines, i, j, direction, i_obstacle= -1, j_obstacle = -1):
    dx, dy = direction
    out_of_bound = is_out_of_bound(lines, i+dx, j+dy)
    if out_of_bound:
        return False, i, j
    found_obstacle = is_obstacle(lines, i+dx, j+dy, i_obstacle, j_obstacle)
    if found_obstacle:
        return False, i, j
    return True, i+dx, j+dy

def walk_guard_to_obstacle(
    lines,
    i0,
    j0,
    direction,
    set_of_visited_positions,
    add_direction=False,
    i_obstacle=-1,
    j_obstacle=-1,
):
    dx, dy = direction
    i, j = i0, j0
    continue_walking = True
    while continue_walking:
        if add_direction:
            set_of_visited_positions.add((i,j, direction))
        else:
            set_of_visited_positions.add((i,j))
        out_of_bound = is_out_of_bound(lines, i+dx, j+dy)
        if out_of_bound:
            return i, j, None # end of game
        continue_walking, i, j = walk_one(lines, i, j, direction, i_obstacle, j_obstacle)
    return i, j, next_direction(direction)

@functools.cache
def walk_to_obstacle_linear(i, list_of_obstacles, dir):
    if dir == 1: # going "forwards"
        higher = [o for o in list_of_obstacles if o > i]
        if len(higher) == 0:
            return -1 # out of bounds
        else:
            return min(higher)-1
    elif dir == -1: # going "backwards"
        lower = [o for o in list_of_obstacles if o < i]
        if len(lower) == 0:
            return -1 # out of bounds
        else:
            return max(lower)+1


def insert_obstacle(obstacles, new_obstacle):
    return [o for o in obstacles if o < new_obstacle] + [new_obstacle] +  [o for o in obstacles if o > new_obstacle]

def walk_guard_to_obstacle_v2(
    obstacles_per_line,
    obstacles_per_column,
    i0,
    j0,
    direction,
    set_of_visited_positions,
    add_direction=False,
    i_obstacle=-1,
    j_obstacle=-1,
):
    if direction in [(-1, 0), (1, 0)]:
        obstacles = insert_obstacle(obstacles_per_column[j0], i_obstacle) if j_obstacle == j0 else obstacles_per_column[j0]
        new_i = walk_to_obstacle_linear(i0, tuple(obstacles), direction[0])
        set_of_visited_positions.update(set([(i, j0) for i in range(i0, new_i, direction[0])]))
        if new_i == -1:
            return i0, j0, None # end of game
        i, j = new_i, j0
    else:
        obstacles = insert_obstacle(obstacles_per_line[i0], j_obstacle) if i_obstacle == i0 else obstacles_per_line[i0]
        new_j = walk_to_obstacle_linear(j0, tuple(obstacles), direction[1])
        set_of_visited_positions.update(set([(i0, j) for j in range(j0, new_j, direction[1])]))
        if new_j == -1:
            return i0, j0, None # end of game
        i, j = i0, new_j
    return i, j, next_direction(direction)

def is_out_of_bound(lines, i, j):
    if i < 0 or j < 0 or i >= len(lines) or j >= len(lines[0]):
        return True
    return False

def get_set_of_visisted_positions(lines):
    i0, j0, dir0 = find_guard(lines)
    set_of_visited_positions = set()
    i, j, direction = i0, j0, dir0
    while True:
        set_of_visited_positions.add((i,j))
        i, j, direction = walk_guard_to_obstacle(lines, i, j, direction, set_of_visited_positions)
        if direction is None:
            break # out of bounds
    return set_of_visited_positions

def is_a_loop(lines, i_obstacle, j_obstacle):
    i0, j0, dir0 = find_guard(lines)
    set_of_visited_positions_with_direction = set()
    i, j, direction = i0, j0, dir0
    while True:
        set_of_visited_positions_with_direction.add((i,j, direction))
        i, j, direction = walk_guard_to_obstacle(
            lines,
            i,
            j,
            direction,
            set_of_visited_positions_with_direction,
            add_direction=True,
            i_obstacle=i_obstacle,
            j_obstacle=j_obstacle,
        )
        if (i,j, direction) in set_of_visited_positions_with_direction:
            return True
        if direction is None:
            return False # out of bounds

def is_a_loop_v2(lines, obstacles_per_line, obstacles_per_column, i_obstacle, j_obstacle):
    i0, j0, dir0 = find_guard(lines)
    set_of_visited_positions_with_direction = set()
    i, j, direction = i0, j0, dir0
    while True:
        set_of_visited_positions_with_direction.add((i,j, direction))
        i, j, direction = walk_guard_to_obstacle_v2(
            obstacles_per_line,
            obstacles_per_column,
            i,
            j,
            direction,
            set_of_visited_positions_with_direction,
            add_direction=True,
            i_obstacle=i_obstacle,
            j_obstacle=j_obstacle,
        )
        if (i,j, direction) in set_of_visited_positions_with_direction:
            # it's a loop !
            return True
        if direction is None:
            return False # out of bounds


def solve_1(input_name: str) -> int:
    # x, i = rows
    # y, j = cols
    lines = process_input(input_name)
    set_of_visited_positions = get_set_of_visisted_positions(lines)
    return len(set_of_visited_positions)

def solve_2(input_name: str) -> int:
    lines = process_input(input_name)
    i0, j0, dir0 = find_guard(lines)
    total = 0
    set_of_visited_positions = get_set_of_visisted_positions(lines)
    for visited_position in set_of_visited_positions:
        # test if an obstacle placed here will create a loop
        i_obstacle, j_obstacle = visited_position
        res = is_a_loop(lines, i_obstacle, j_obstacle)
        if res:
            total += 1
    return total

def better_solve_2(input_name):
    lines = process_input(input_name)
    obstacles_per_line = get_obstacles_per_line(lines)
    obstacles_per_column = get_obstacles_per_column(lines)
    total = 0
    set_of_visited_positions = get_set_of_visisted_positions(lines)
    for visited_position in set_of_visited_positions:
        # test if an obstacle placed here will create a loop
        i_obstacle, j_obstacle = visited_position
        res = is_a_loop_v2(lines, obstacles_per_line, obstacles_per_column, i_obstacle, j_obstacle)
        if res:
            total += 1
    return total


if __name__ == "__main__":
    import time
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    start = time.time()
    value_2 = solve_2(input_name="input.txt")
    end = time.time()
    print("Part 2, small input:", value_2, "- took", end-start, "seconds")
    start = time.time()
    value_2 = better_solve_2(input_name="input.txt")
    end = time.time()
    print("Part 2:", value_2, "- took", end-start, "seconds")
