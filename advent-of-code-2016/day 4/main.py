"""Advent of Code 2016 Day 4."""
from collections import defaultdict


def main(file_input='input.txt'):
    rooms = [parse_room(line.strip())
             for line in get_file_contents(file_input)]
    valid_rooms = validate_rooms(rooms)
    sector_ids_sum = sum_sector_ids(valid_rooms)
    print(f'Sum of sector IDs of the real rooms: {sector_ids_sum}')
    decrypted_rooms = [(decrypt_room(room), room) for room in valid_rooms]
    north_pole = [
        (decrypted, room)
        for decrypted, room in decrypted_rooms
        if 'north' in decrypted
    ][0]
    print('Sector ID of room with North Pole object stored: '
          f'{north_pole[1][0]}')


def decrypt_room(room):
    """Decrypt name using the sector ID or the room."""
    id, name, _ = room
    decrypted = []
    for word in name:
        cur_word = [shift_letter(letter, id) for letter in word]
        decrypted.append(''.join(cur_word))
    return ' '.join(decrypted)


def shift_letter(letter, shift):
    """Shift letter by shift number."""
    base = ord('a')
    num_letters_in_alphabet = 26
    return chr(base + (ord(letter) - base + shift) % num_letters_in_alphabet)


def is_room_valid(room):
    """Check if room is valid."""
    _, names, checksum = room
    letters = defaultdict(int)
    complete_name = ''.join(names)
    for letter in complete_name:
        letters[letter] += 1
    sorted_alphabetic = sorted(letters)
    sorted_by_occurrences = sorted(
        sorted_alphabetic, key=letters.__getitem__, reverse=True)
    return ''.join(sorted_by_occurrences).startswith(checksum)


def sum_sector_ids(rooms):
    """Sum sector IDs."""
    return sum(id for id, name, checksum in rooms)


def validate_rooms(rooms):
    """Return validated rooms."""
    return [room
            for room in rooms
            if is_room_valid(room)]


def parse_room(line):
    """Parse room from line to tuple with id, name and checksum."""
    *name, id_checksum = line.split('-')
    id, checksum = id_checksum[:-1].split('[')
    return (int(id), name, checksum)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
