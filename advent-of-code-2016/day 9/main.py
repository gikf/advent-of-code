"""Advent of Code 2016 Day 9."""
import re


def main(file_input='input.txt'):
    line = get_file_contents(file_input)[0].strip()
    decompressed = count_decompression(line)
    print(f'Decompressed length: {decompressed}')
    decompressed_deep = count_decompression(line, True)
    print(f'Decompressed length using version two: {decompressed_deep}')


def count_decompression(line, deep=False):
    """Decompress line, with optional deeper decompression.

    If deep is True decompresses also sequences inside of
    the decompressed subsequence.
    """
    result = 0
    index = 0
    cur_sequence = ''
    while index < len(line):
        if line[index] == '(':
            result += len(cur_sequence)
            cur_sequence = ''
        elif line[index] == ')':
            length, repeats = [
                int(num) for num in re.findall(r'(\d+)x(\d+)', cur_sequence)[0]
            ]
            cur_sequence = ''
            decompressed = count_part(line[index + 1:index + 1 + length], deep)
            result += decompressed * repeats
            index += length
        else:
            cur_sequence += line[index]
        index += 1
    return result + len(cur_sequence)


def count_part(sequence, deep):
    """Count sequence or decompress it deeper."""
    if deep:
        return count_decompression(sequence, deep)
    return len(sequence)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
