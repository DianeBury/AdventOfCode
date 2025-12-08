from operator import mul
from functools import reduce


def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()

    numbers = [
        [int(e) for e in line.rstrip().split(" ") if e != ""] for line in lines[:-1]
    ]
    operations = [e for e in lines[-1].rstrip().split(" ") if e != ""]

    for line in numbers:
        if len(operations) != len(line):
            raise ValueError

    return numbers, operations


def solve_1(input_name: str, verbose: bool = False) -> int:
    numbers, operations = process_input(input_name)
    printv(verbose, numbers)
    printv(verbose, operations)
    results = []
    for i, op in enumerate(operations):
        printv(verbose, i, ":", op)
        if op == "+":
            res = sum([line[i] for line in numbers])
            results.append(res)
        else:
            res = reduce(mul, [line[i] for line in numbers], 1)
            results.append(res)
        printv(verbose, [line[i] for line in numbers], "-->", res)
    return sum(results)


def process_input2(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()
    numbers = [line.rstrip("\n") for line in lines[:-1]]
    operations = [e for e in lines[-1].rstrip().split(" ") if e != ""]
    N = len(numbers[0])
    for line in numbers:
        assert N == len(line), ValueError
    return numbers, operations


def apply(op, res, number):
    if op == "+":
        return res + number
    elif op == "*":
        return res * number
    raise ValueError


def solve_2(input_name: str, verbose: bool = False) -> int:
    numbers, operations = process_input2(input_name)

    nb_lines = len(numbers)
    current_op_index = 0
    current_operation = operations[current_op_index]
    current_result = 0 if current_operation == "+" else 1
    printv(verbose, "current operation = ", current_operation)
    results = []

    for i in range(len(numbers[0])):
        current_text = ""
        for j in range(nb_lines):
            current_text += numbers[j][i]

        if current_text.replace(" ", "") == "":
            results.append(current_result)
            current_op_index += 1
            current_operation = operations[current_op_index]
            current_result = 0 if current_operation == "+" else 1
            printv(verbose, "current operation = ", current_operation)
            continue

        current_number = int(current_text)
        current_result = apply(current_operation, current_result, current_number)
        printv(verbose, current_number, "-->", current_result)

    results.append(current_result)
    printv(verbose, results)
    return sum(results)


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=True)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=True)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
