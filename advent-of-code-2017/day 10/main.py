"""Advent of Code 2017 Day 10."""


def main(file_input='input.txt'):
    list_ = [num for num in range(256)]

    lengths = [int(num) for num in get_file_contents(file_input)[0].split(',')]
    result, position, skip = knot_list(list_[:], lengths)
    print(f'Two first numbers in list multiplied: {result[0] * result[1]}')

    lengths_ascii = (
        [ord(char) for char in get_file_contents(file_input)[0].strip()]
        + [17, 31, 73, 47, 23])
    sparse_hash = rounds(list_[:], lengths_ascii, 64)
    dense_hash = get_dense_hash(sparse_hash)
    print(f'Dense hash: {dense_hash}')


def get_dense_hash(sparse_hash):
    """Get dense hash from sparse hash."""
    dense_hash = []
    cur_number = None
    counter = 0
    for number in sparse_hash:
        if counter == 15:
            cur_number = cur_number ^ number
            hexed = hex(cur_number)[2:]
            dense_hash.append(f'{hexed:0>2}')
            cur_number = None
            counter = 0
            continue

        if cur_number is None:
            cur_number = number
        else:
            cur_number = cur_number ^ number
        counter += 1
    return ''.join(dense_hash)


def rounds(list_, lengths, rounds):
    """Perform knotting number of rounds on list_ using lengths values."""
    position = 0
    skip = 0
    for _ in range(rounds):
        _, position, skip = knot_list(list_, lengths, position, skip)
    return list_


def knot_list(list_, lengths, position=0, skip=0):
    """Knot list_ using lengths values, starting with position and skip."""
    wrap_at = len(list_)
    for length in lengths:
        start = position
        end = position + length
        if end > wrap_at:
            reverse_with_wrap(list_, start, end, wrap_at)
        else:
            list_[start:end] = list_[start:end][::-1]
        position = (position + length + skip) % wrap_at
        skip += 1
    return list_, position, skip


def reverse_with_wrap(list_, start, end, wrap_at):
    """Reverse list_ from start to end wrapping back to beginning of list."""
    length_to_end = wrap_at - start
    length_from_start = end % wrap_at
    reverse = (list_[start:] + list_[:length_from_start])[::-1]
    list_[start:] = reverse[0:length_to_end]
    list_[:length_from_start] = reverse[length_to_end:]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
