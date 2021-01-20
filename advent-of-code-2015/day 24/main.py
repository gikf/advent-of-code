"""Advent of Code 2015 Day 24."""
from itertools import combinations


def main(file_input='input.txt'):
    packages = {int(line.strip()) for line in get_file_contents(file_input)}
    total_weight = sum(packages)
    lowest_for_3 = get_lowest_entanglement_for_shortest_group(
        packages, total_weight, 3)
    print(lowest_for_3)
    lowest_for_4 = get_lowest_entanglement_for_shortest_group(
        packages, total_weight, 4)
    print(lowest_for_4)


def get_lowest_entanglement_for_shortest_group(packages, total_weight, groups):
    """Get lowest entanglement for groups from packages.

    Each group sums to total_weight divided by number of groups.
    """
    packagings = get_shortest_size_groups_with_sum(
        packages, total_weight / groups)
    packagings_by_quantum = sorted(packagings, key=get_quantum_entanglement)
    return ('Lowest quantum entanglement for shortest group for weight '
            f'split by {groups}: '
            f'{get_quantum_entanglement(packagings_by_quantum[0])}, '
            f'({packagings_by_quantum[0]})')


def get_shortest_size_groups_with_sum(packages, target, group_size=1):
    """Get packages groups with lowest group_size that sum to target."""
    while group_size < len(packages):
        possible_combs = [combination
                          for combination in combinations(packages, group_size)
                          if sum(combination) == target]
        if possible_combs:
            return possible_combs
        group_size += 1
    return None


def get_quantum_entanglement(containers):
    """Quantum entanglement of containers."""
    result = 1
    for container in containers:
        result *= container
    return result


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
