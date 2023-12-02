import re

digits = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_value(line: str):
    # Need to find all overlapping digits, so we use a lookahead
    matches = re.finditer("(?=([0-9]|" + "|".join(digits.keys()) + "))", line.lower())
    results = [match.group(1) for match in matches]
    a = results[0]
    if a in digits:
        a = digits[a]
    b = results[-1]
    if b in digits:
        b = digits[b]
    value = int(a) * 10 + int(b)
    return value


def solve():
    total_value = 0
    with open("input_1.txt", "r") as f:
        for line in f:
            total_value += get_value(line)
    return total_value


if __name__ == "__main__":
    value = solve()
    print(value)
