from functools import lru_cache


def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()
    return [line.rstrip() for line in lines]


def solve_1(input_name: str, verbose: bool = False) -> int:
    lines = process_input(input_name)
    for line in lines:
        printv(verbose, line)
    nb_split = 0
    current_beams = set()
    first_line = lines[0]
    max_index = len(lines[0]) - 1
    beam_index = first_line.index("S")
    printv(verbose, "Tachyon beam at index", beam_index)
    current_beams.add(beam_index)
    for i, line in enumerate(lines[1:]):
        printv(verbose, "Line", i + 1, ":", current_beams)
        for beam_index in current_beams.copy():
            if line[beam_index] == "^":
                # split !
                printv(verbose, "Split at index", beam_index)
                nb_split += 1
                current_beams.remove(beam_index)
                for splitted_beam in [beam_index - 1, beam_index + 1]:
                    if 0 <= splitted_beam and splitted_beam <= max_index:
                        current_beams.add(splitted_beam)
    return nb_split


@lru_cache(maxsize=None)
def count_timelines(beam_index: int, lines: tuple[str]) -> int:
    if len(lines) == 0:
        return 1
    else:
        if lines[0][beam_index] == "^":
            # split !
            return count_timelines(beam_index - 1, lines[1:]) + count_timelines(
                beam_index + 1, lines[1:]
            )
        else:
            return count_timelines(beam_index, lines[1:])


def solve_2(input_name: str, verbose: bool = False) -> int:
    lines = process_input(input_name)
    for line in lines:
        printv(verbose, line)
    first_line = lines[0]
    beam_index = first_line.index("S")
    res = count_timelines(beam_index, tuple(lines[1:]))
    return res


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=True)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
