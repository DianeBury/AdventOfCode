def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()
    reports = [[int(e) for e in line.split(" ")] for line in lines]
    return reports

def is_report_valid_1(report: list):
    # Report is safe if the differences between two consecutive values are either all positive or all negative
    # and no diff is bigger than 3 (in absolute)
    diff = [i - j for i,j in zip(report[:-1], report[1:])]
    positive = [e > 0 and e < 4 for e in diff]
    negative = [e < 0 and e > -4 for e in diff]
    if all(positive) or all(negative):
        return True
    return False

def solve_1(input_name: str) -> int:
    reports = process_input(input_name)
    valids = [is_report_valid_1(report) for report in reports]
    return sum([1 if e else 0 for e in valids])

def is_report_valid_2(report: list):
    if is_report_valid_1(report):
        return True
    for i in range(len(report)):
        alt_report = report[0:i] + report[i+1:]
        if is_report_valid_1(alt_report):
            # Removing value report[i] makes the report safe
            return True
    return False

def solve_2(input_name: str) -> int:
    reports = process_input(input_name)
    valids = [is_report_valid_2(report) for report in reports]
    return sum([1 if e else 0 for e in valids])

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
