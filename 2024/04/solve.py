def process_input(input_name: str) -> list[str]:
    with open(input_name, "r") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
    return lines

def test_letter(lines: list[str], x:int, y:int, words:list[str], direction: tuple[int, int]=None) -> int:
    """Counts the number of times one of the given word appears starting at (x,y).

    Several words can be given. If the letter at (x,y) corresponds to
    the first letter of one of the words, the test continues with that word.
    If a direction is given, test only in that direction. In that case the answer can be only 0 or 1.
    """
    # handle edge cases : x or y out of bounds
    if x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0]):
        return 0
    for word in words:
        if len(word) == 1:
            # check if letter at (x,y) is the wanted letter
            return 1 if lines[x][y] == word[0] else 0
    for word in words:
        if lines[x][y] == word[0]:
            # the letter at (x,y) is correct
            if direction is None:
                # check all the surrounding letters
                total = 0
                for dx in range(-1,2):
                    for dy in range(-1,2):
                        if dx == 0 and dy == 0:
                            continue
                        total += test_letter(lines, x+dx, y+dy, [word[1:]], direction=(dx,dy))
                return total
            else:
                # check only in the given direction
                dx, dy = direction
                return test_letter(lines, x+dx, y+dy, [word[1:]], direction)
    return 0

def solve_1(input_name: str) -> int:
    lines = process_input(input_name)
    total = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            n = test_letter(lines, i, j, ["XMAS"])
            total += n
    return total

def solve_2(input_name: str) -> int:
    lines = process_input(input_name)
    total = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            res1 = test_letter(lines, i, j, ["MAS", "SAM"], direction=(1,1))
            if res1 == 1:
                res2 = test_letter(lines, i, j+2, ["MAS", "SAM"], direction=(1,-1))
                total += res2
    return total

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
