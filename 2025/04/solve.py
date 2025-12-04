def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def get_neighbors_index(x: int, y: int) -> list[tuple[int, int]]:
    return [
        (x + i, y + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i != 0 or j != 0)
    ]


def is_in_grid(pos: tuple[int, int], nb_lines: int, nb_cols: int) -> bool:
    x, y = pos
    return x >= 0 and y >= 0 and x < nb_lines and y < nb_cols


def process_input(input_name: str):
    grid = []
    with open(input_name, "r") as f:
        for line in f:
            processed_line = [0 if e == "." else 1 for e in line.rstrip()]
            grid.append(processed_line)
    return grid


def count_rolls(
    grid: list[list[int]],
    neighbors: dict[tuple[int, int], int],
    verbose: bool = False,
) -> int:
    nb_accessible_rolls = 0
    nb_lines = len(grid)
    nb_cols = len(grid[0])
    for i in range(nb_lines):
        line = ""
        for j in range(nb_cols):
            nb = neighbors[(i, j)]
            nb = neighbors.get((i, j), -1)
            if nb >= 4:
                e = "@"
            elif nb >= 0:
                e = "x"
                nb_accessible_rolls += 1
            else:
                e = "."
            line += e + " "
        printv(verbose, line)
    return nb_accessible_rolls


def solve_1(input_name: str, verbose: bool = False) -> int:
    grid = process_input(input_name)
    neighbors = count_neighbors(grid)
    res = count_rolls(grid, neighbors, verbose)
    return res


def remove_accessible_rolls(
    grid: list[list[int]],
    neighbors: dict[tuple[int, int], int],
    verbose: bool = False,
) -> int:
    # Update grid by removing accessible rolls
    nb_accessible_rolls = 0
    nb_lines = len(grid)
    nb_cols = len(grid[0])
    for i in range(nb_lines):
        line = ""
        for j in range(nb_cols):
            nb = neighbors.get((i, j), -1)
            if nb >= 4:  # inaccessible
                e = "@"
            elif nb >= 0:  # accessible !
                grid[i][j] = -1  # remove roll !
                e = "x"
                nb_accessible_rolls += 1
            else:  # no roll
                e = "."
            line += e + " "
        # printv(verbose, line)
    return nb_accessible_rolls


def count_neighbors(grid: list[list[int]]) -> dict[tuple[int, int], int]:
    neighbors = {}
    # Count neighbors
    for i, line in enumerate(grid):
        for j, e in enumerate(line):
            if e == 1:  # roll at (i,j)
                if not (i, j) in neighbors:
                    neighbors[(i, j)] = 0
                for nb in get_neighbors_index(i, j):
                    nbs = neighbors.get(nb, 0)
                    if nbs != -1:  # increment the neighbor count
                        neighbors[nb] = nbs + 1
            else:  # no roll at (i,j)
                neighbors[(i, j)] = (
                    -1  # to indicate there is no roll there, no need to count the neighbors
                )
    return neighbors


def solve_2(input_name: str, verbose: bool = False) -> int:
    grid = process_input(input_name)
    total_removable_rolls = 0
    i = 0
    while True:
        printv(verbose, "Iter", i)
        neighbors = count_neighbors(grid)
        nb_accessible_rolls = remove_accessible_rolls(grid, neighbors, verbose)
        printv(verbose, "  accesible rolls : ", nb_accessible_rolls)
        if nb_accessible_rolls == 0:
            break
        total_removable_rolls += nb_accessible_rolls
    return total_removable_rolls


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=False)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
