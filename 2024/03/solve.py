import re

def process_input(input_name: str) -> list[str]:
    with open(input_name, "r") as f:
        lines = f.readlines()
    return lines

def process_line(line: str, regex: str) -> int:
    # identify all valid instructions
    res = re.findall(regex, line)
    total_sum = 0
    for mul in res:
        # get the two numbers
        x = re.match(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", mul)
        a = int(x.group(1))
        b = int(x.group(2))
        total_sum += a*b
    # return the sum of the product of each instruction
    return total_sum

def solve_1(input_name: str) -> int:
    lines = process_input(input_name)
    total_sum = 0
    exp = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    for line in lines:
        total_sum += process_line(line, exp)
    return total_sum

def solve_2(input_name: str) -> int:
    lines = process_input(input_name)
    total_sum = 0
    exp = r"mul\([0-9]{1,3},[0-9]{1,3}\)"
    # Joining all lines because do / don't instructions are apply
    # from one line to the other
    big_line = ''.join(lines)
    no_do_inside = big_line.split("do()")
    for substring in  no_do_inside:
        do = substring.split("don't()")[0]
        total_sum += process_line(do, exp)
    return total_sum

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input2.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
