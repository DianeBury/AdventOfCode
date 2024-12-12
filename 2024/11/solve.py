import functools
from functools import wraps
import time

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

@functools.lru_cache
def get_nb_digits(a: int) -> int:
    if a < 10:
        return 1
    return 1 + get_nb_digits(a // 10)

def process_input(input_name: str):
    with open(input_name, "r") as f:
        stones = [int(e) for e in f.readline().replace("\n", "").split(" ")]
    return stones

@functools.lru_cache
def process_one_stone(stone: int):
    nb_digits = get_nb_digits(stone)
    if stone == 0:
        # Stone is engraved with number 0
        return [1]
    elif nb_digits % 2 == 0:
        # Stone is engraved with a number that has an even number of digits
        engraving = str(stone)
        return [int(e) for e in [engraving[:nb_digits//2], engraving[nb_digits//2:]]]
    else:
        return [stone * 2024]


nb_baby_stones = {}
@functools.lru_cache
def count_children_stone_for_n_blinks(stone: int, blinks: int):
    """Return the number of stones created by the input stone in the given number of blinks."""
    if blinks == 0:
        return 1
    if (stone, blinks) in nb_baby_stones:
        return nb_baby_stones[(stone, blinks)]
    stones = process_one_stone(stone)
    total = 0
    for s in stones:
        total += count_children_stone_for_n_blinks(s, blinks-1)
    nb_baby_stones[(stone, blinks)] = total
    return total

@timeit
def solve_1(input_name: str) -> int:
    stones = process_input(input_name)
    nb_blinks = 25
    for _ in range(nb_blinks):
        new_stones = []
        for stone in stones:
            new_stones.extend(process_one_stone(stone))
        stones = new_stones
    return len(stones)


@timeit
def solve_2(input_name: str) -> int:
    stones = process_input(input_name)
    nb_blinks = 75
    total = 0
    for stone in stones:
        total += count_children_stone_for_n_blinks(stone, nb_blinks)
    return total


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)