import re


def get_score(n: int) -> int:
    if n == 0:
        return 0
    return pow(2, (n - 1))


def get_number_matching_numbers(line: str) -> int:
    res = re.match("Card\s+[0-9]+: (.*) \| (.*)", line)
    winning_numbers = [int(v) for v in res.groups()[0].split() if v != ""]
    my_numbers = [int(v) for v in res.groups()[1].split() if v != ""]
    my_winning_numbers = set(my_numbers) & set(winning_numbers)
    return len(my_winning_numbers)


def solve_1(input_name: str) -> int:
    # Process each line, use sets to find matching numbers
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            if line == "\n":
                continue
            nb_matching_numbers = get_number_matching_numbers(line)
            score = get_score(nb_matching_numbers)
            value += score
    return value


def solve_2(input_name: str) -> int:
    # Same as 1, but we keep a dict of future additional copies won, as well
    # as a dict of how many copies we got for each card
    processed_copies = {}
    unprocessed_additional_copies = {}
    with open(input_name, "r") as f:
        for index, line in enumerate(f):
            index = index + 1
            additional_copies = unprocessed_additional_copies.setdefault(index, 0)
            total_copies = 1 + additional_copies
            processed_copies[index] = total_copies
            nb_matching_numbers = get_number_matching_numbers(line)
            # print(f"Card {index} has {nb_matching_numbers} winning numbers, total copies = {total_copies}")
            for i in range(index + 1, index + nb_matching_numbers + 1):
                # print(f"Adding {total_copies} copies to card {i}")
                nb = unprocessed_additional_copies.setdefault(i, 0)
                unprocessed_additional_copies[i] = nb + total_copies
    return sum(processed_copies.values())


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
