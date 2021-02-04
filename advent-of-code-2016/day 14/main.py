"""Advent of Code 2016 Day 14."""
import hashlib
import re


puzzle = 'zpqevtbw'


def main(salt=puzzle):
    pad_key = find_nth_pad_key(puzzle, 64)
    print(f'Index producing 64th key: {pad_key[0]}')
    pad_key = find_nth_pad_key(puzzle, 64, 2017)
    print(f'Index producing 64th key with hashing 2017 times: {pad_key[0]}')


def find_nth_pad_key(salt, key_number, stretch=1):
    """Find key_number key using salt and stretch number times hashing."""
    keys = []
    hashes = []
    index = 0
    while len(keys) < key_number:
        while True:
            if len(hashes) <= index:
                hashes.append(get_hash(salt, index, stretch))
            repeat_check = is_repeating(hashes[index], r'[\w\d]', 3)
            if repeat_check:
                hash_index = index + 1000
                repeating_char = repeat_check[0]
                break
            index += 1
        while len(hashes) <= hash_index:
            hashes.append(get_hash(salt, len(hashes), stretch))
        for index_to_check in range(index + 1, hash_index + 1):
            if is_repeating(hashes[index_to_check], repeating_char, 5):
                keys.append((index, hashes[index]))
                break
        index += 1
    return keys[-1]


def is_repeating(text, char, number_times):
    """Find char or regex group num_times in row in text."""
    regex = fr'({char})\1{{{number_times - 1}}}'
    result = re.findall(regex, text)
    if result:
        return result
    return None


def get_hash(salt, index, stretch):
    """Hash seed with appended index stretch number of times."""
    result = f'{salt}{index}'
    for _ in range(stretch):
        result = hashlib.md5(result.encode()).hexdigest()
    return result


if __name__ == '__main__':
    main()
