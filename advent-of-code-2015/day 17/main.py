"""Advent of Code 2015 Day 17."""


def main(file_input='input.txt'):
    containers = [int(line.strip()) for line in get_file_contents(file_input)]
    combinations = find_fills(150, containers, [])
    print('Number of combinations to fill 150 liters of eggnog: '
          f'{len(combinations)}')
    minimum_number_of_containers = min(map(len, combinations))
    minimum_containers_used = [
        combination for combination in combinations
        if len(combination) == minimum_number_of_containers
    ]
    print('Number of combinations using minimum number '
          f'of containers: {len(minimum_containers_used)}')


def find_fills(liters, containers, containers_used):
    """Find combinations of containers to fit entirely liters of eggnog."""
    if liters == 0:
        return [containers_used]
    elif liters < 0 or not containers:
        return []

    cur_containers = containers_used + [containers[0]]
    results = []
    next_fills = (
        (liters - containers[0], containers[1:], cur_containers),
        (liters, containers[1:], containers_used)
    )
    for fill in next_fills:
        results.extend(find_fills(*fill))
    return results


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
