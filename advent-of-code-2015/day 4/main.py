"""Advent of Code 2015 Day 4."""
import hashlib


def main():
    key = 'bgvyzdsv'
    number = get_number_suffix(key, startwith='00000')
    print(f'Lowest number making hash start with five zeros {number}')
    number6 = get_number_suffix(key, startwith='000000', start_number=number)
    print(f'Lowest number making hash start with six zeros {number6}')


def get_number_suffix(key, startwith, start_number=1):
    """Get number suffix of key making hash start with startwith."""
    number = start_number
    while not get_md5(f'{key}{number}').startswith(startwith):
        number += 1
    return number


def get_md5(text):
    """Get md5 hash of text."""
    return hashlib.md5(text.encode()).hexdigest()


if __name__ == '__main__':
    main()
