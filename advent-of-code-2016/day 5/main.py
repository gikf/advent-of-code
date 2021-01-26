"""Advent of Code 2016 Day 5."""
import hashlib


puzzle = 'ugkcyxxp'


def main(puzzle=puzzle):
    password = find_password(puzzle, next_empty)
    print(f'Password: {password}')
    password_not_in_order = find_password(puzzle, without_order)
    print(f'Password found not in order: {password_not_in_order}')


def find_password(door_id, decrypter):
    """Find password for door_id, using decrypter function."""
    password = [None] * 8
    index = 0
    while not all(password):
        next_hash = hashlib.md5(f'{door_id}{index}'.encode()).hexdigest()
        if next_hash.startswith('0' * 5):
            position, char = decrypter(password, next_hash)
            if is_position_valid(position, password):
                password[position] = char
        index += 1
    return ''.join(password)


def is_position_valid(position, password):
    """Check if position is valid for password."""
    return 0 <= position < len(password) and password[position] is None


def next_empty(password, hash):
    """Find next empty position in password and value to fill it with.

    Returns tuple with two elements - int position and character for password.
    """
    return password.index(None), hash[5]


def without_order(password, hash):
    """Find position of the next character from the hash and value to fill.

    Returns tuple with two elements - int position and character for password.
    """
    position = int(hash[5]) if hash[5].isdigit() else -1
    return position, hash[6]


if __name__ == '__main__':
    main()
