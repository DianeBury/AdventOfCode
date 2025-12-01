def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str) -> list[int]:
    # L = left  = -
    # R = right = +
    # example: rotations = [-68, -30, +48]
    rotations = []
    with open(input_name, "r") as f:
        for line in f.readlines():
            rot = int(line[1:])
            if line[0] == "L":
                rot *= -1
            rotations.append(rot)
    return rotations


def apply_rotation(current_pos: int, rotation: int) -> int:
    return (current_pos + rotation) % 100


def apply_rotation_and_count_zero(
    current_pos: int, rotation: int, verbose: bool = False
) -> tuple[int, int]:
    passes_by_zero = 0
    simple_rotation = rotation % 100 if rotation > 0 else (rotation % 100) - 100
    passes_by_zero = abs(rotation) // 100
    new_pos = current_pos + simple_rotation
    printv(verbose, "rotation =", rotation, ": ", current_pos, "->", new_pos)
    if rotation > 0:
        new_pos = current_pos + simple_rotation
        if new_pos > 100:
            passes_by_zero += 1
    elif rotation < 0:
        if new_pos < 0 and current_pos > 0:
            passes_by_zero += 1
    printv(verbose, "    passes by zero", passes_by_zero, "times")
    return (current_pos + rotation) % 100, passes_by_zero


def solve_1(input_name: str) -> int:
    rotations = process_input(input_name)
    current_position = 50
    password = 0

    for rot in rotations:
        current_position = apply_rotation(current_position, rot)
        if current_position == 0:
            password += 1

    return password


def solve_2(input_name: str, verbose: bool = False) -> int:
    rotations = process_input(input_name)
    current_position = 50
    password = 0

    for rot in rotations:
        current_position, passes_by_zero = apply_rotation_and_count_zero(
            current_position, rot, verbose
        )
        password += passes_by_zero
        if current_position == 0:
            password += 1
    return password


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=True)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
