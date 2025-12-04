def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)

def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()
    return lines

def solve_1(input_name: str, verbose: bool = False) -> int:
    lines = process_input(input_name)
    printv(verbose, lines)
    res = 0
    return res

def solve_2(input_name: str, verbose: bool = False) -> int:
    lines = process_input(input_name)
    printv(verbose, lines)
    res = 0
    return res


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=False)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
