"""Advent of Code 2016 Day 16."""


puzzle = '11101000110010100'


def main(initial_state=puzzle):
    disk_lengths = [272, 35651584]
    for disk in disk_lengths:
        state = fill_disk(initial_state, disk)
        checksum = get_checksum(state)
        print(f'Checksum for disk of length {disk}: {checksum}')


def fill_disk(state, disk_size):
    """Fill disk_size disk with sequence based on the initial state.

    Repeats until state is longer than disk_size:
    - Call the data you have at this point "a".
    - Make a copy of "a"; call this copy "b".
    - Reverse the order of the characters in "b".
    - In "b", replace all instances of 0 with 1 and all 1s with 0.
    - The resulting data is "a", then a single 0, then "b".
    """
    while len(state) < disk_size:
        a = state
        b = ''.join('1' if char == '0' else '0' for char in a[::-1])
        state = f'{a}0{b}'
    return state[:disk_size]


def get_checksum(state):
    """Get checksum from the state.

    Compares pairs of characters, passing 1 to checksum if they are the same
    0 otherwise. Process repeats until length of checksum is odd.
    """
    checksum = []
    for index, _ in enumerate(state[::2]):
        if state[index * 2] == state[index * 2 + 1]:
            checksum.append('1')
        else:
            checksum.append('0')
    if len(checksum) % 2 == 0:
        return get_checksum(checksum)
    return ''.join(checksum)


if __name__ == '__main__':
    main()
