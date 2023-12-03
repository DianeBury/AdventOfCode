IS_SYMBOL = {}
GRID = {}
NUMBERS = {}
STARS = []


def create_number(string: str, row: int, col: int, length: int):
    return {"string": string, "row": row, "col": col, "length": length}


def get_numbers(line: str, row_id: int = 0):
    numbers = []
    found_number = False
    for i in range(len(line)):
        if line[i].isdigit():
            if found_number is False:
                found_number = True
                numbers.append(create_number(line[i], row_id, i, 1))
            else:
                n = numbers[-1]
                n["string"] = n["string"] + line[i]
                n["length"] += 1
        else:
            found_number = False
    return numbers


def get_periphery(number: dict, nb_rows: int, nb_cols: int) -> list:
    length = number["length"]
    row = number["row"]
    col = number["col"]
    points = []
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + length + 1):
            if not out_of_range(nb_rows, nb_cols, (i, j)):
                points.append((i, j))
    return points


def out_of_range(nb_rows: int, nb_cols: int, point: list) -> bool:
    if point[0] < 0 or point[0] >= nb_rows or point[1] < 0 or point[1] >= nb_cols:
        return True
    return False


def is_symbol(lines, point):
    res = IS_SYMBOL.get(point)
    if res is None:
        char = lines[point[0]][point[1]]
        res = (not char.isdigit()) and char != "."
        IS_SYMBOL[point] = res
    return res


def solve_1(input_name: str) -> int:
    with open(input_name, "r") as f:
        lines = f.readlines()
    lines = [l for l in lines if l != "\n"]
    nb_rows = len(lines)
    nb_cols = len(lines[0].strip())
    value = 0
    for row, line in enumerate(lines):
        numbers = get_numbers(line, row)
        for n in numbers:
            points = get_periphery(n, nb_rows, nb_cols)
            for point in points:
                if is_symbol(lines, point):
                    value += int(n["string"])
                    break
    return value


def add_n_to_grid(number: dict) -> None:
    n = int(number["string"])
    row = number["row"]
    col = number["col"]
    n_id = len(NUMBERS)
    for i in range(col, col + number["length"]):
        GRID[(row, i)] = n_id
        NUMBERS[n_id] = n


def get_stars(line: str) -> list:
    return [i for i in range(len(line)) if line[i] == "*"]


def solve_2(input_name: str) -> int:
    with open(input_name, "r") as f:
        lines = f.readlines()
    lines = [l for l in lines if l != "\n"]

    nb_rows = len(lines)
    nb_cols = len(lines[0].strip())
    value = 0

    # Build the lists of numbers (with their coordinates) and of stars
    for row, line in enumerate(lines):
        numbers = get_numbers(line, row)
        # The grid has for key the coordinates of point part of a number, and for values
        # the id of the number it contains
        # We keep another dict for numbers, id -> actual value of the number
        for n in numbers:
            add_n_to_grid(n)
        STARS.extend([(row, j) for j in get_stars(line)])
    # We iterate over the stars and check their neighbors for numbers
    for s in STARS:
        sn = create_number("*", s[0], s[1], 1)
        points = get_periphery(sn, nb_rows, nb_cols)
        distinct_neighbor_numbers_id = set([GRID[p] for p in points if p in GRID])
        distinct_neighbor_numbers = [
            NUMBERS[pid] for pid in distinct_neighbor_numbers_id
        ]
        if len(distinct_neighbor_numbers) == 2:
            value += distinct_neighbor_numbers[0] * distinct_neighbor_numbers[1]
    return value


if __name__ == "__main__":
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
