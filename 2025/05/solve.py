def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str):
    ranges = []
    ingredients = []
    with open(input_name, "r") as f:
        for line in f:
            if line.rstrip() == "":
                break
            ranges.append([int(e) for e in line.rstrip().split("-")])
        for line in f:
            ingredients.append(int(line.rstrip()))
    return ranges, ingredients


def solve_1(input_name: str, verbose: bool = False) -> int:
    ranges, ingredients = process_input(input_name)
    printv(verbose, ranges)
    printv(verbose, ingredients)
    fresh_ingredients = []
    for ing in ingredients:
        for start, end in ranges:
            if start <= ing and ing <= end:
                fresh_ingredients.append(ing)
                break
    printv(verbose, fresh_ingredients)
    return len(fresh_ingredients)


def collision(interval1, interval2) -> bool:
    if interval2[0] <= interval1[0] and interval1[0] <= interval2[1]:
        return True
    if interval2[0] <= interval1[1] and interval1[1] <= interval2[1]:
        return True
    if (
        interval1[1] == interval2[0] - 1 or interval2[1] == interval1[0] - 1
    ):  # they touch
        return True
    if interval1[0] <= interval2[0] and interval2[1] <= interval1[1]:
        return True
    if interval2[0] <= interval1[0] and interval1[1] <= interval2[1]:
        return True
    return False


def fusion(interval1, interval2):
    return (min(interval1[0], interval2[0]), max(interval1[1], interval2[1]))


def fusion_multiple(intervals):
    if len(intervals) == 0:
        return []
    elif len(intervals) == 1:
        return intervals[0]
    elif len(intervals) == 2:
        return fusion(intervals[0], intervals[1])
    else:
        return fusion_multiple([fusion(intervals[0], intervals[1])] + intervals[2:])


def add_interval(interval_list: list[tuple[int, int]], new_interval: tuple[int, int], verbose:bool = False):
    new_list = []
    if len(interval_list) == 0:
        return [new_interval]
    collision_intervals = [new_interval]
    for existing_interval in interval_list:
        if collision(existing_interval, new_interval):
            collision_intervals.append(existing_interval)
        else:
            new_list.append(existing_interval)
    fusionned = fusion_multiple(collision_intervals)
    new_list.append(fusionned)
    return new_list


def total_count(interval_list):
    if len(interval_list) == 0:
        return 0
    interval = interval_list[0]
    return interval[1] - interval[0] + 1 + total_count(interval_list[1:])


def solve_2(input_name: str, verbose: bool = False) -> int:
    ranges, _ = process_input(input_name)
    printv(verbose, ranges)

    interval_list = []
    count = 0
    for fresh_range in ranges:
        printv(verbose, interval_list)
        printv(verbose, "  adding", fresh_range)
        interval_list = add_interval(interval_list, fresh_range, verbose)
        new_count = total_count(interval_list)
        if not count <= new_count:
            raise ValueError
        count = total_count(interval_list)

    printv(verbose, interval_list)
    return total_count(interval_list)


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=True)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=True)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
