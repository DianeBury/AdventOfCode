import math

def to_int_list(a_string: str, delimiter:str = " ") -> list[int]:
    return [int(e) for e in a_string.split(delimiter) if e != ""]

def process_input(input_name: str) -> tuple[list[int], list[int]]:
    with open(input_name, "r") as f:
        time_line = f.readline()
        distance_line = f.readline()
    times = to_int_list(time_line.replace("Time:", ""))
    distances = to_int_list(distance_line.replace("Distance:", ""))
    return times, distances

def process_input2(input_name: str) -> tuple[int]:
    with open(input_name, "r") as f:
        time_line = f.readline()
        distance_line = f.readline()
    total_time = int(time_line.replace("Time:", "").replace(" ", ""))
    best_distance = int(distance_line.replace("Distance:", "").replace(" ", ""))
    return total_time, best_distance

def get_solutions(total_time: int, best_distance: int) -> list[int]:
    # Finding how long to hold a button to beat the best distance
    # for a race of time T is equivalent to solving the inequality:
    # t^2 - T * t + best_distance < 0
    # also, t < 0 does not make sense
    determinant = total_time*total_time - 4*best_distance
    x1 = (total_time - math.sqrt(determinant)) / 2
    x2 = (total_time + math.sqrt(determinant)) / 2
    sols = [i for i in range(int(math.fabs(x1))+1, int(math.fabs(x2))+1)]
    if x2 in sols: sols.remove(x2)
    if x1 in sols: sols.remove(x1)
    return sols

def get_number_solutions(total_time: int, best_distance: int) -> int:
    # Finding how long to hold a button to beat the best distance
    # for a race of time T is equivalent to solving the inequality:
    # t^2 - T * t + best_distance < 0
    # also, t < 0 does not make sense
    determinant = total_time*total_time - 4*best_distance
    x1 = (total_time - math.sqrt(determinant)) / 2
    x2 = (total_time + math.sqrt(determinant)) / 2
    # get first and last integer to be solutions
    i1 = int(x1) + 1
    if x2 == int(x2):
        i2 = int(x2) - 1
    else:
        i2 = int(x2)
    nb_solutions = i2 - i1 + 1
    return nb_solutions

def solve_1(input_name: str) -> int:
    times, distances = process_input(input_name)
    res = 1
    for t, d in zip (times, distances):
        solutions = get_solutions(t, d)
        res *= len(solutions)
    return res

def solve_2(input_name: str) -> int:
    total_time, best_distance = process_input2(input_name)
    return get_number_solutions(total_time, best_distance)


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
