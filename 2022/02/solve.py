TO_ABC = {"X": "A", "Y": "B", "Z": "C"}
WIN_AGAINST = {"A": "C", "B": "A", "C": "B"}
SHAPE_SCORE = {"A": 1, "B": 2, "C": 3}
OUTCOME_SCORE = {"X": 0, "Y": 3, "Z": 6}
LOSE_AGAINST = {l:w for w,l in WIN_AGAINST.items()}


def get_outcome_score(opponent: str, you: str) -> int:
    if you in TO_ABC:
        you = TO_ABC[you]
    if opponent == you:
        # draw
        return 3
    elif WIN_AGAINST[opponent] == you:
        # you lose
        return 0
    elif WIN_AGAINST[you] == opponent:
        # you win
        return 6
    else:
        raise RuntimeError("This should not happen!")


def get_round_score(opponent: str, you: str) -> int:
    if you in TO_ABC:
        you = TO_ABC[you]
    shape_score = SHAPE_SCORE[you]
    outcome_score = get_outcome_score(opponent, you)
    return shape_score + outcome_score


def solve_1(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            opponent, you = line.strip("\n").split(" ")
            value += get_round_score(opponent, you)
    return value


def get_your_move(opponent: str, outcome: str) -> str:
    if outcome == "X":
        return WIN_AGAINST[opponent]
    elif outcome == "Y":
        return opponent
    elif outcome == "Z":
        return LOSE_AGAINST[opponent]
    else:
        raise ValueError("This should not happen")


def solve_2(input_name: str) -> int:
    value = 0
    with open(input_name, "r") as f:
        for line in f:
            opponent, outcome = line.strip("\n").split(" ")
            you = get_your_move(opponent, outcome)
            score = get_round_score(opponent, you)
            value += score
    return value


if __name__ == "__main__":
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
