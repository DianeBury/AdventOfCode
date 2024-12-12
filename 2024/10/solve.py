import functools

def process_input(input_name: str) -> tuple[tuple[tuple[int, ...]], list[tuple[int, int]]]:
    grid = []
    zeros = []
    with open(input_name, "r") as f:
        grid = tuple([tuple([int(e) for e in line.replace("\n", "")]) for line in f.readlines()])
    zeros = [(i,j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    return grid, zeros

def neighbors(x: int, y: int) -> list[tuple[int, int]]:
    """Return up, down, left, right neighbors."""
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def is_out_of_bounds(grid: tuple[tuple[int, ...]], i: int, j: int) -> bool:
    return i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0])

@functools.lru_cache
def find_nines(grid: tuple[tuple[int, ...]], i: int, j: int) -> list[tuple[int, int]]:
    """Return the list of all 9 attainable through hiking trails from the given positions.
    This list can contain double of the same 9, if severals trails lead to it."""
    trails = []
    if is_out_of_bounds(grid, i, j):
        return []
    starting_number = grid[i][j]
    if starting_number == 9:
        if grid[i][j] == 9:
            return [(i,j)]
    for next_i, next_j in neighbors(i,j):
        if is_out_of_bounds(grid, next_i, next_j):
            continue
        if grid[next_i][next_j] == starting_number + 1:
            trails.extend(find_nines(grid, next_i, next_j))
    return trails

def solve_1(input_name: str) -> int:
    grid, zeros = process_input(input_name)
    sum_scores = 0
    for i0,j0 in zeros:
        # iterate over all zeros in the grid
        nines = find_nines(grid, i0, j0)
        nb_unique_nines = len(set(nines))
        sum_scores += nb_unique_nines
    return sum_scores

def solve_2(input_name: str) -> int:
    grid, zeros = process_input(input_name)
    sum_scores = 0
    for i0,j0 in zeros:
        # iterate over all zeros in the grid
        nines = find_nines(grid, i0, j0)
        nb_trails = len(nines)
        sum_scores += nb_trails
    return sum_scores

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
