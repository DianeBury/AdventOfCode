from typing import Union
import copy

def process_input(input_name: str) -> list[list[Union[int, bool]]]:
    disk = []
    with open(input_name, "r") as f:
        line = f.readline()
        file = True
        current_id = 0
        for char in line:
            n = int(char)
            if file:
                disk.append([n, current_id]) # n blocks for file current_id
                current_id += 1
                file = False
            else:
                disk.append([n, -1]) # n empty blocks (-1 corresponds to empty space)
                file = True
    return disk

def is_empty(block_group: list[Union[int, bool]]) -> bool:
    return block_group[1] == -1

def remove_empty_blocks_at_the_end(disk: list[Union[int, bool]]) -> None:
    last_block_group = disk[-1]
    if is_empty(last_block_group):
        index = len(disk) -1
        disk.pop(index)
        remove_empty_blocks_at_the_end(disk)
    else:
        return

def find_next_empty_space(disk: list[Union[int, bool]], index: int) -> int:
    if index >= len(disk):
        return -1
    for i in range(index, len(disk)):
        if is_empty(disk[i]):
            return i
    return -1

def pretty_string(disk: list[Union[int, bool]]) -> str:
    pretty_string = ""
    for group in disk:
        if is_empty(group):
            pretty_string += "." * group[0]
        else:
            pretty_string += str(group[1]) * group[0]
    return pretty_string

def one_step(disk: list[Union[int, bool]], index_empty_space: int, file_index: int = -1) -> int:
    """Move blocks from the end of the disk to the chosen empty space.
    If there is more empty blocks than blocks of the last file, then some empty blocks remain.
    If there is more blocks of the last file at the end than empty blocks, then some blocks of the file remain.
    """
    n_empty = disk[index_empty_space][0]
    n_file = disk[file_index][0]
    if n_empty < n_file:
        # Fewer empty blocks than file blocks: empty blocks are all filled by the file and there are leftover file blocks
        # change id of empty space to file id
        disk[index_empty_space][1] = disk[file_index][1]
        # update size of last file
        disk[file_index][0] -= n_empty
    if n_empty >= n_file:
        # File is wholly moved
        file_group = copy.copy(disk[file_index])
        # replace file blocks by empty blocks
        disk[file_index][1] = -1
        if n_empty == n_file:
            # As many empty blocks as file blocks: change id of empty space to file id
            disk.pop(index_empty_space)
        elif n_empty > n_file:
            # More empty blocks than file blocks: there are leftover empty blocks
            # insert file group before updated empty space
            # Update size of empty group
            disk[index_empty_space][0] -= n_file
        disk.insert(index_empty_space, file_group)
    remove_empty_blocks_at_the_end(disk)
    return find_next_empty_space(disk, index_empty_space)

def next_file_index(disk: list[Union[int, bool]], index_file_to_move: int, current_id: int) -> int:
    """Find the index of the first file before the index_file_to_move (going backwards)."""
    for i in range(1, index_file_to_move + 1):
        if index_file_to_move - i >= len(disk):
            continue
        if disk[index_file_to_move - i][1] != -1 and disk[index_file_to_move - i][1] < current_id:
            # found a file
            return index_file_to_move - i
    return -1

def find_available_empty_space(disk: list[Union[int, bool]], n_file: int) -> int:
    for i, group in enumerate(disk):
        if is_empty(group) and group[0] >= n_file:
            return i
    return -1

def one_step_whole_file(disk: list[Union[int, bool]], index_file_to_move: int) -> int:
    """Attempt to move one whole file from the end of the disk to the first large enough empty space."""
    index_file_to_move = index_file_to_move
    current_id = disk[index_file_to_move][1]
    if disk[index_file_to_move][2]:
        # File has already been moved / tried to be moved
        return next_file_index(disk, index_file_to_move, current_id)
    # Note that the file has been processed
    disk[index_file_to_move][2] = True
    n_file = disk[index_file_to_move][0]
    idx_chosen_space = find_available_empty_space(disk, n_file)
    if idx_chosen_space >= 0 and idx_chosen_space < index_file_to_move:
        # There is at least one big-enough empty space, move whole file
        # There may be empty blocks before and after that need to be joined
        if index_file_to_move > 0 and index_file_to_move < len(disk)-1:
            if is_empty(disk[index_file_to_move-1]) and is_empty(disk[index_file_to_move+1]):
                # join two empty blocks groups into one
                disk[index_file_to_move-1][0] += disk[index_file_to_move+1][0]
                disk.pop(index_file_to_move+1)

        one_step(disk, idx_chosen_space, index_file_to_move)
    else:
        pass
    return next_file_index(disk, index_file_to_move, current_id)

def checksum(disk: list[Union[int, bool]]) -> int:
    starting_idx = 0
    checksum = 0
    for group in disk:
        if group[1] != -1:
            checksum += sum((starting_idx+i)* group[1] for i in range(group[0]))
        starting_idx += group[0]
    return checksum

def solve_1(input_name: str) -> int:
    disk = process_input(input_name)
    # All operations on the disk are made in place
    index_first_empty_space = 1
    while True:
        index_first_empty_space = one_step(disk, index_first_empty_space)
        n = len(disk)
        if index_first_empty_space == -1 or index_first_empty_space >= n:
            break
    return checksum(disk)

def solve_2(input_name: str) -> int:
    disk = process_input(input_name)
    disk = [[group[0], group[1], False] for group in disk] # group size, group ID, whether group has been moved/tested for move
    # All operations on the disk are made in place
    index_file_to_move = len(disk)-1
    while True:
        index_file_to_move = one_step_whole_file(disk, index_file_to_move)
        if index_file_to_move <= 0:
            break
    return checksum(disk)

if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt")
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt")
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt")
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt")
    print("Part 2:", value_2)
