def does_1_contain_2(elf1, elf2):
    s1, e1 = elf1
    s2, e2 = elf2
    if s1 <= s2 and e2 <= e1:
        return True


def does_1_overlap_2(elf1, elf2):
    s1, e1 = elf1
    s2, e2 = elf2
    if s1 <= s2 and s2 <= e1:
        return True


def solve_1(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            print(line)
            elf1, elf2 = line.strip("\n").split(",")
            elf1 = [int(i) for i in elf1.split("-")]
            elf2 = [int(i) for i in elf2.split("-")]
            print(elf1, " - ", elf2)
            if does_1_contain_2(elf1, elf2) or does_1_contain_2(elf2, elf1):
                value += 1
    return value


def solve_2(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            elf1, elf2 = line.strip("\n").split(",")
            elf1 = [int(i) for i in elf1.split("-")]
            elf2 = [int(i) for i in elf2.split("-")]
            if does_1_overlap_2(elf1, elf2) or does_1_overlap_2(elf2, elf1):
                value += 1
    return value


if __name__ == "__main__":
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
