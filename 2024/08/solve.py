import itertools

def process_input(input_name: str) -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    antennas = {}
    with open(input_name, "r") as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.replace("\n", "")):
                if c != ".":
                    antennas.setdefault(c, []).append((i,j))
    return antennas, i+1, j+1

def is_in_bounds(point: int, size_i: int, size_j: int) -> bool:
    return point[0] >= 0 and point[0] < size_i and point[1] >= 0 and point[1] < size_j

def get_antinodes(a1: tuple[int, int], a2: tuple[int, int], multiple: int = 1) -> tuple[tuple[int, int], tuple[int, int]]:
    i1, j1 = a1
    i2, j2 = a2
    anti1 = i1 - multiple*(i2-i1), j1 - multiple*(j2-j1)
    anti2 = i2 - multiple*(i1-i2), j2 - multiple*(j1-j2)
    return anti1, anti2

def solve_1(input_name: str) -> int:
    antennas, size_i, size_j = process_input(input_name)
    antinodes = set()
    for a in antennas:
        combi = itertools.combinations(antennas[a], 2)
        for antenna1, antenna2 in combi:
            anti1, anti2 = get_antinodes(antenna1, antenna2)
            for anti in [anti1, anti2]:
                if is_in_bounds(anti, size_i, size_j):
                    antinodes.add(anti)
    return len(antinodes)

def solve_2(input_name: str) -> int:
    antennas, size_i, size_j = process_input(input_name)
    antinodes = set()
    for a in antennas:
        combi = itertools.combinations(antennas[a], 2)
        for antenna1, antenna2 in combi:
            k = 0
            while True:
                anti1, anti2 = get_antinodes(antenna1, antenna2, k)
                anti1_in = is_in_bounds(anti1, size_i, size_j)
                anti2_in = is_in_bounds(anti2, size_i, size_j)
                if anti1_in:
                    antinodes.add(anti1)
                if anti2_in:
                    antinodes.add(anti2)
                if not anti1_in and not anti2_in:
                    break
                k += 1
    return len(antinodes)

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
