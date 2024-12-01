def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()

    l1 = [[int(e) for e in line.split("   ")][0] for line in lines]
    l2 = [[int(e) for e in line.split("   ")][1] for line in lines]
    return l1, l2

def solve_1(input_name: str) -> int:
    l1, l2 = process_input(input_name)
    l1.sort()
    l2.sort()

    res = sum([abs(e1 - e2) for e1,e2 in zip(l1, l2)])
    return res

def solve_2(input_name: str) -> int:
    l1, l2 = process_input(input_name)
    res = 0
    for e in l1:
        n = l2.count(e)
        res += e * n
    return res


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
