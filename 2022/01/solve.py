def get_elves(input_name: str):
    elves = [[]]
    with open(input_name, "r") as f:
        for line in f:
            if line == "\n":
                elves.append([])
            else:
                elves[-1].append(int(line.strip("\n")))
    return elves


def solve_1(input_name: str):
    elves = get_elves(input_name)
    calories_by_elf = [sum(v) for v in elves]
    max_calories = max(calories_by_elf)
    idx = calories_by_elf.index(max_calories)
    return max_calories


def solve_2(input_name: str):
    elves = get_elves(input_name)
    calories_by_elf = [sum(v) for v in elves]
    calories_by_elf.sort(reverse=True)
    top_three = calories_by_elf[0:3]
    return sum(top_three)


if __name__ == "__main__":
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
