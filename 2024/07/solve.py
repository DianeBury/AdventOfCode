def power_of_ten(a: int) -> int:
    if a < 10:
        return 0
    return 1 + power_of_ten(a // 10)

def process_input(input_name: str) -> list[tuple[int, list[int]]]:
    with open(input_name, "r") as f:
        lines = [line.replace("\n", "") for line in f.readlines()]
        operations = []
        for line in lines:
            result = int(line.split(":")[0])
            numbers = [int(e) for e in line.split(": ")[1].split(" ")]
            operations.append((result, numbers))
    return operations

def is_valid_recursive(result: int, numbers: list[int], use_concatenation:bool=False) -> bool:
    if len(numbers) == 1:
        return result == numbers[0]
    n = numbers[-1]
    if use_concatenation:
        # Test concatenation
        exp = power_of_ten(n)
        if (result - n) % (10**(exp+1)) == 0: # result last digits are the ones of n
            res = is_valid_recursive((result - n)//(10**(exp+1)), numbers[:-1], use_concatenation)
            if res:
                return True
    # Test multiplication
    if result % n == 0: # result is a multiple of first number
        res = is_valid_recursive(result // n, numbers[:-1], use_concatenation)
        if res:
            return True
    # Test addition
    if result - n >= 0:
        res = is_valid_recursive(result - n, numbers[:-1], use_concatenation)
        if res:
            return True
    return False

def solve_1(input_name: str) -> int:
    operations = process_input(input_name)
    total = 0
    for result, numbers in operations:
        valid = is_valid_recursive(result, numbers)
        if valid:
            total += result
    return(total)

def solve_2(input_name: str) -> int:
    operations = process_input(input_name)
    total = 0
    for result, numbers in operations:
        valid = is_valid_recursive(result, numbers, use_concatenation=True)
        if valid:
            total += result
    return(total)

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
