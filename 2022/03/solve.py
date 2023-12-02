import string
import itertools

PRIORITY = {}


def build_priorities():
    for letter in string.ascii_lowercase:
        PRIORITY[letter] = ord(letter) - ord("a") + 1
    for letter in string.ascii_uppercase:
        PRIORITY[letter] = ord(letter) - ord("A") + 27


def get_compartments(line: str):
    line = line.strip("\n")
    length = len(line) // 2
    return line[:length], line[length:]


def solve_1(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            comp1, comp2 = get_compartments(line)
            set1 = set([l for l in comp1])
            set2 = set([l for l in comp2])
            error = (set1 & set2).pop()
            priority = PRIORITY[error]
            value += priority
    return value


def solve_2(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for lines in itertools.zip_longest(*[f] * 3):
            sets = []
            for line in lines:
                sets.append(set([l for l in line.strip("\n")]))
            badge = (sets[0] & sets[1] & sets[2]).pop()
            value += PRIORITY[badge]
    return value


if __name__ == "__main__":
    build_priorities()
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
