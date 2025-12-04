
def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str):
    banks = []
    with open(input_name, "r") as f:
        for line in f:
            banks.append([int(e) for e in line.rstrip()])
    return banks


def solve_1(input_name: str, verbose: bool = False) -> int:
    banks = process_input(input_name)
    total_joltage = 0
    for bank in banks:
        printv(verbose, bank[:-1])
        battery1 = max(bank[:-1])
        max_bat_index = bank.index(battery1)
        right_bank = bank[max_bat_index+1:]
        battery2 = max(right_bank)
        max_joltage = 10 * battery1 + battery2
        printv(verbose, "  max joltage =", max_joltage)
        total_joltage += max_joltage
    return total_joltage

def solve_2(input_name: str, verbose: bool = False) -> int:
    banks = process_input(input_name)
    N_bat = 12
    total_joltage = 0
    for bank in banks:
        printv(verbose, bank)
        batteries = []
        current_bank = bank
        for i in range(N_bat):
            # Search for the i-th battery in the remaining available bank
            if N_bat-i-1 == 0:
                # Last battery to find, we use the rest of the bank
                printv(verbose, "  i =", i, " - current bank available = ", current_bank)
                bat = max(current_bank)
            else:
                printv(verbose, "  i =", i, " - current bank available = ", current_bank[:-(N_bat-i-1)])
                bat = max(current_bank[:-(N_bat-i-1)])
            bat_index = current_bank.index(bat)
            printv(verbose, "    max bat = ", bat, " at index", bat_index)
            batteries.append(bat)
            current_bank = current_bank[bat_index+1:]
        max_joltage = sum([bat * 10**j for j, bat in enumerate(batteries[::-1])])
        printv(verbose, "  max joltage =", max_joltage)
        total_joltage += max_joltage
    return total_joltage


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=False)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
