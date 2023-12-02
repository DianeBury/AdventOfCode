def pretty_print_stack(stacks: dict) -> None:
    max_nb_crates = max([len(v) for v in stacks.values()])
    lines = [" " + "   ".join([str(k) for k in stacks.keys()])]
    for i in range(max_nb_crates):
        lines.append(
            " " + "   ".join([v[i] if len(v) > i else " " for v in stacks.values()])
        )
    lines = lines[::-1]
    for l in lines:
        print(l)


def get_nb_initial_lines(input_name: str) -> int:
    nb_lines = 0
    with open(input_name, "r") as f:
        for line in f:
            if line == "\n":
                break
            nb_lines += 1
    return nb_lines


def read_initial_stack(input_name: str) -> (dict, int):
    # Find number of lines used to describe initial stack
    nb_lines = get_nb_initial_lines(input_name)
    with open(input_name, "r") as f:
        head = [next(f).strip("\n") for _ in range(nb_lines)]
    # reverse the lines, to add the crates from the bottom up
    head = head[::-1]
    stacks = {int(s): [] for s in head[0].strip().split("   ")}
    for line in head[1:]:
        crates = {s: line[1 + 4 * (s - 1)] for s in stacks}
        for i in crates:
            if crates[i] != " ":
                stacks[i].append(crates[i])
    return stacks, nb_lines


def move(stacks: dict, from_i: int, to_i: int) -> None:
    crate = stacks[from_i].pop()
    stacks[to_i].append(crate)


def move_together(stacks: dict, from_i: int, to_i: int, nb: int) -> None:
    # pop crates
    crates = [stacks[from_i].pop() for _ in range(nb)]
    # reverse to go back to original order
    crates = crates[::-1]
    # add to stack
    stacks[to_i].extend(crates)


def process_line(line: str) -> (int, int, int):
    _, nb, _, from_i, _, to_i = line.strip().split()
    return int(nb), int(from_i), int(to_i)


def solve_1(input_name: str) -> str:
    stacks, nb_head_lines = read_initial_stack(input_name)
    with open(input_name, "r") as f:
        [next(f) for _ in range(nb_head_lines + 1)]
        for line in f:
            nb, from_i, to_i = process_line(line)
            for _ in range(nb):
                move(stacks, from_i, to_i)
    top_crates = [s[-1] for s in stacks.values()]
    return "".join(top_crates).replace(" ", "")


def solve_2(input_name: str) -> str:
    stacks, nb_head_lines = read_initial_stack(input_name)
    with open(input_name, "r") as f:
        [next(f) for _ in range(nb_head_lines + 1)]
        for line in f:
            nb, from_i, to_i = process_line(line)
            move_together(stacks, from_i, to_i, nb)

    top_crates = [s[-1] for s in stacks.values()]
    return "".join(top_crates).replace(" ", "")


if __name__ == "__main__":
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
