def process_input(input_name: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules = []
    updates = []
    with open(input_name, "r") as f:
        while True:
            line = f.readline()
            if line == "\n":
                # blank line between rules and updates
                break
            a, b = [int(e) for e in line.split("|")]
            rules.append((a,b))
        while True:
            line = f.readline()
            if line in ["", "\n"]:
                # end of file
                break
            updates.append([int(e) for e in line.split(",")])
    return rules, updates

def get_list_of_pages_after(rules: list[tuple[int, int]], update: list[int]) -> dict[int, set[int]]:
    """Returns a dictionary that links each page to the list of pages that must be after.
    Only considers the rules that applies to the given update."""
    pages_after = {} # for each page, list of pages that must be after
    for a,b in rules:
        if a in update and b in update:
            pages_after.setdefault(a, set()).add(b)
    return pages_after

def is_update_ordered(rules: list[tuple[int, int]], update: list[int]) -> bool:
    pages_after = get_list_of_pages_after(rules, update)
    for i, page in enumerate(update):
        # check that all the pages before page i in the update
        # are not in the list of pages that must be after page i
        if page not in pages_after:
            continue
        for p in update[:i]:
            if p in pages_after[page]:
                return False
    return True

def reorder_update(rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    pages_after = get_list_of_pages_after(rules, update)
    nb_of_dependencies = {}
    for page in update:
        if page in pages_after:
            nb_of_dependencies[page] = len(pages_after[page]) 
        else:
            nb_of_dependencies[page] = 0
    sorted_update = [k for k,_ in sorted(nb_of_dependencies.items(), key=lambda item:item[1], reverse=True)]
    return sorted_update

def solve_1(input_name: str) -> int:
    rules, updates = process_input(input_name)
    total = 0
    # for k,v in rules.items():
    #     print(k, ":", v)
    for update in updates:
        res = is_update_ordered(rules, update)
        if res:
            middle_page = update[len(update)//2]
            total += middle_page
    return total

def solve_2(input_name: str) -> int:
    rules, updates = process_input(input_name)
    total = 0
    for update in updates:
        res = is_update_ordered(rules, update)
        if res:
            # ordered update, pass
            continue
        # consider only unordered updates
        sorted_update = reorder_update(rules, update)
        middle_page = sorted_update[len(update)//2]
        total += middle_page
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
