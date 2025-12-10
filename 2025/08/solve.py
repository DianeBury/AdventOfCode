import bisect


def printv(verbose: bool = False, *toprint) -> None:
    if verbose:
        print(*toprint)


def process_input(input_name: str):
    with open(input_name, "r") as f:
        lines = f.readlines()
    points = [tuple([int(e) for e in line.rstrip().split(",")]) for line in lines]
    return points


def squared_distance(p1: tuple[int], p2: tuple[int]) -> int:

    return sum([(p1[i] - p2[i]) ** 2 for i in range(3)])


def get_circuit(circuits, p):
    for circ in circuits:
        if p in circ:
            return circ
    circ = set([p])
    circuits.append(circ)
    return circ


def solve_1(input_name: str, N: int = 1000, verbose: bool = False) -> int:
    points = process_input(input_name)
    printv(verbose, points)

    distances = {}
    sorted_pairs = []  # sorted list of the N closest pairs
    circuits = []

    for i, p1 in enumerate(points):
        for p2 in points:
            if p1 == p2 or (p2, p1) in distances:
                continue
            distances[(p1, p2)] = squared_distance(p1, p2)
            if len(sorted_pairs) < N:
                # populate the sorted list with N values
                bisect.insort(sorted_pairs, (p1, p2), key=lambda x: distances[x])
            else:
                # if new pair distance is smaller than the biggest distance in the current sorted_list:
                # remove biggest distance and insert new distance
                if distances[(p1, p2)] < distances[sorted_pairs[-1]]:
                    sorted_pairs = sorted_pairs[:-1]
                    bisect.insort(sorted_pairs, (p1, p2), key=lambda x: distances[x])
            printv(verbose, sorted_pairs)

    # sorted_points = sorted(distances.keys(), key=lambda x: distances[x])

    for i in range(N):
        # try to connect the two points
        p1, p2 = sorted_pairs[i][0], sorted_pairs[i][1]
        printv(verbose, "\nPoints : ", p1, p2)
        # add p2 (and its circuit) to circuit of p1
        circuit1 = get_circuit(circuits, p1)
        printv(verbose, "circuit1 = ", circuit1)
        circuit2 = get_circuit(circuits, p2)
        printv(verbose, "circuit2 = ", circuit2)
        if circuit1 == circuit2:
            pass
        else:
            for p in get_circuit(circuits, p2):
                circuit1.add(p)
            circuits.remove(circuit2)

        printv(verbose, "Circuits = ", circuits)

    circuits_count = {}
    for circ in circuits:
        circuits_count[len(circ)] = circuits_count.get(len(circ), 0) + 1

    res = 1
    for k in sorted(circuits_count.keys(), reverse=True)[:3]:
        res *= k
    return res


def solve_2(input_name: str, verbose: bool = False) -> int:
    points = process_input(input_name)
    # printv(verbose, points)
    Npoints = len(points)

    distances = {}
    circuits = []
    sorted_pairs = []

    for i, p1 in enumerate(points):
        for p2 in points:
            if p1 == p2 or (p2, p1) in distances:
                continue
            distances[(p1, p2)] = squared_distance(p1, p2)

    sorted_pairs = sorted(distances.keys(), key=lambda x: distances[x])

    all_in_one_circuit = False
    count = 0
    while not all_in_one_circuit:
        printv(verbose, "\nPair", count)
        # try to connect the two points
        p1, p2 = sorted_pairs[count][0], sorted_pairs[count][1]
        count += 1
        printv(verbose, "Points : ", p1, p2)
        # add p2 (and its circuit) to circuit of p1
        circuit1 = get_circuit(circuits, p1)
        printv(verbose, "circuit1 = ", circuit1)
        circuit2 = get_circuit(circuits, p2)
        printv(verbose, "circuit2 = ", circuit2)
        if circuit1 == circuit2:
            pass
        else:
            for p in get_circuit(circuits, p2):
                circuit1.add(p)
            circuits.remove(circuit2)

        if len(circuits) == 1 and len(circuits[0]) == Npoints:
            all_in_one_circuit = True

    res = p1[0] * p2[0]
    return res


if __name__ == "__main__":
    value_1 = solve_1(input_name="small_input.txt", N=10, verbose=False)
    print("Part 1, small input:", value_1)
    value_1 = solve_1(input_name="input.txt", verbose=False)
    print("Part 1:", value_1)
    value_2 = solve_2(input_name="small_input.txt", verbose=False)
    print("Part 2, small input:", value_2)
    value_2 = solve_2(input_name="input.txt", verbose=False)
    print("Part 2:", value_2)
