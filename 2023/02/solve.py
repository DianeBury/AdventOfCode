import copy

COLORS = ["red", "green", "blue"]


def get_id_and_sets(line: str):
    game_id = int(line.split(":")[0].split(" ")[1])
    sets = line.split(":")[1]
    sets = sets.split(";")
    return game_id, sets


def get_nb_and_color(text: str):
    # text is of format "N color"
    for color in ["blue", "red", "green"]:
        if color in text:
            N = int(text.split(" " + color)[0].strip())
            return N, color
    return 0, None


def is_set_possible(all_cubes, one_set: str):
    for text in one_set.split(","):
        N, color = get_nb_and_color(text)
        if N > all_cubes[color]:
            return False
    return True


def is_game_possible(all_cubes, line: str):
    possible = True
    game_id, sets = get_id_and_sets(line)
    for one_set in sets:
        possible = is_set_possible(all_cubes, one_set)
        if not possible:
            return game_id, False
    return game_id, True


def solve_1(**all_cubes):
    sum_ids = 0
    with open("input_1.txt", "r") as f:
        for line in f:
            game_id, possible = is_game_possible(all_cubes, line)
            if possible:
                sum_ids += game_id
    return sum_ids


def get_cubes_in_set(one_set: str):
    cubes = {color: 0 for color in COLORS}
    for text in one_set.split(","):
        N, color = get_nb_and_color(text)
        cubes[color] = N
    return cubes


def merge_cubes_sets(cubes1, cubes2):
    merged_cubes = copy.copy(cubes1)
    for color in cubes1:
        assert color in cubes2
        merged_cubes[color] = max(cubes1[color], cubes2[color])
    return merged_cubes


def power(cubes: dict):
    value = 1
    for color in COLORS:
        nb = cubes.setdefault(color, 0)
        value *= nb
    return value


def solve_2():
    sum_of_powers = 0
    with open("input_1.txt", "r") as f:
        for line in f:
            _, sets = get_id_and_sets(line)
            minimum_cubes_in_set = {color: 0 for color in COLORS}
            for one_set in sets:
                cubes = get_cubes_in_set(one_set)
                minimum_cubes_in_set = merge_cubes_sets(minimum_cubes_in_set, cubes)
            sum_of_powers += power(minimum_cubes_in_set)
    return sum_of_powers


if __name__ == "__main__":
    value1 = solve_1(red=12, green=13, blue=14)
    print(value1)
    value2 = solve_2()
    print(value2)
