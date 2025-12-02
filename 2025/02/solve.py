import math


def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def nb_digit(n: int) -> int:
    return 1 + math.floor(math.log10(n))


def get_pattern(sequence: int, nb_repetition: int = 2):
    res = 0
    nb_digits = nb_digit(sequence)
    for i in range(0, nb_repetition):
        res += sequence * 10 ** (i * nb_digits)
    return res


def add_range(ranges: list[tuple[int, int]], new_range: tuple[int, int]):
    (range_start, range_end) = new_range
    RS_nb_digits = nb_digit(range_start)
    RE_nb_digits = nb_digit(range_end)
    if RS_nb_digits == RE_nb_digits:
        ranges.append((range_start, range_end))
    else:
        ranges.append((range_start, (10**RS_nb_digits) - 1))
        add_range(ranges, (10**RS_nb_digits, range_end))
    return


def process_input(input_name: str):
    with open(input_name, "r") as f:
        line = f.readlines()[0]
    ranges = [[int(val) for val in e.split("-")] for e in line.split(",")]
    return ranges


def process_input_modified(input_name: str):
    with open(input_name, "r") as f:
        line = f.readlines()[0]
    ranges = [[int(val) for val in e.split("-")] for e in line.split(",")]
    # Modify the ranges so that there is no range for which the start and end value have different number of digits
    new_ranges = []
    for range_start, range_end in ranges:
        add_range(new_ranges, (range_start, range_end))
    return new_ranges


def solve_1(input_name: str, verbose: bool = False) -> int:
    ranges = process_input(input_name)
    invalid_ids = []
    for range_start, range_end in ranges:
        printv(verbose, (range_start, range_end))
        # Find the minimal amount of digit for the sequence that is repeated twice for a silly pattern
        # ex: for range [95, 115] the minimal amount of digit for the repeated sequence is 1
        # ex: for range [998, 1012], the minimal amount of digit for the repeated sequence is 2
        RS_nb_digits = nb_digit(range_start)
        nb_digit_min = RS_nb_digits // 2
        if RS_nb_digits % 2 != 0:
            nb_digit_min = (RS_nb_digits + 1) // 2
        # Find the maximal amount of digit for the sequence that is repeated twice
        # ex: for range [95, 115], the maximal amomunt of digit for the repeated sequence is 1
        # ex: for range [998, 1012], the maximal amount of digit for the repeated sequence is 2
        RE_nb_digits = nb_digit(range_end)
        nb_digit_max = RE_nb_digits // 2
        if RE_nb_digits % 2 != 0:
            nb_digit_max = (RE_nb_digits - 1) // 2
        # If the invalid ID id between range_start and range_end then
        # range_start / (1 + 10^(1+nb_digit_max)) <= invalid ID <= range_end / (1 + 10^(1+nb_digit_min))
        start_pattern = math.ceil(range_start / (1 + 10 ** (nb_digit_max)))
        end_pattern = math.floor(range_end / (1 + 10 ** (nb_digit_min)))

        if nb_digit_max < nb_digit_min:
            # no invalid ID in this range, for example if the start value and end value of the range
            # have the same odd number of digits
            printv(verbose, "---")
            continue

        # the repeated sequence needs to have at least nb_digit_min digits, and cannot be lower than start_pattern
        start_sequence = max(start_pattern, 10 ** (nb_digit_min - 1))
        # the repeated sequence cannot have more than nb_digits_max digits, and cannot be higher than end_pattern
        end_sequence = min(end_pattern, 10 ** (nb_digit_max) - 1)

        # Go through all the possible repeated sequences to create invalid IDs
        for i in range(
            start_sequence,
            end_sequence + 1,
        ):
            n = 1 + math.floor(math.log10(i))
            silly_id = i * (1 + 10**n)
            printv(verbose, i, "->", silly_id)
            if silly_id < range_start or silly_id > range_end:
                raise ValueError
            invalid_ids.append(silly_id)
        printv(verbose, "---")
    return sum(invalid_ids)


def solve_2(input_name: str, verbose: bool = False) -> int:
    # This ensures each range in ranges has start and end values with the same number of digits
    ranges = process_input_modified(input_name)

    invalid_ids = set()
    for range_start, range_end in ranges:
        printv(verbose, (range_start, range_end))
        nb_digits = nb_digit(range_start)
        if nb_digits != nb_digit(range_end):
            raise ValueError

        nb_digit_max = nb_digits // 2
        if nb_digits % 2 != 0:
            nb_digit_max = (nb_digits - 1) // 2
        for i in range(1, nb_digit_max + 1):
            # Finding repeated sequences with i digits
            # printv(verbose, "sequences with", i, "digits")
            if nb_digits % i != 0:
                # Can't repeat X times sequence with i digits to obtain RS_nb_digits
                continue
            else:
                nb_repetition = nb_digits // i
            starting_sequence = 10 ** (i - 1)
            ending_sequence = (10**i) - 1
            # Testing all the sequences of i digits repeated nb_repetition times
            for seq in range(starting_sequence, ending_sequence + 1):
                pattern = get_pattern(seq, nb_repetition)
                if pattern < range_start:
                    continue
                if pattern > range_end:
                    break
                if not pattern in invalid_ids:
                    printv(verbose, "  invalid id :", pattern)
                    invalid_ids.add(pattern)
    return sum(invalid_ids)


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=False)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
