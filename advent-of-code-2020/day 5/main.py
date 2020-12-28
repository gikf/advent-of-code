# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 18:39:27 2020
"""


def main():
    seats = parse_seats(get_file_contents())
    seat_ids = [get_seat_id(*seat) for seat in seats]
    print(missing_seats(seat_ids))
    print(max(seat_ids))


def parse_seats(seats):
    """Parse list of text input seats."""
    return [parse_seat(seat) for seat in seats]


def parse_seat(seat):
    """Parse single seat"""
    return (
        binary_search(seat[:-3], 0, 127, 'F', 'B'),
        binary_search(seat[-3:], 0, 7, 'L', 'R')
    )


def binary_search(string, num_minimum, num_maximum, lower, higher):
    """Use binary search to find number representation of string.

    Returns number in range num_minimum and num_maximum after
    partitioning range based on string and characters lower and higher
    indication which end of range to partition."""
    for part in string:
        middle = (num_minimum + num_maximum) // 2
        if part == lower:
            num_maximum = middle
        elif part == higher:
            num_minimum = middle + 1
    if part == lower:
        return num_minimum
    else:
        return num_maximum


def missing_seats(seat_ids):
    """Find missing seat id in the seat_ids."""
    reference = {seat_id for seat_id in range(
        min(seat_ids), max(seat_ids) + 1)}
    return reference - set(seat_ids)


def get_seat_id(row, column):
    """Get seat id from row and column."""
    return row * 8 + column


def get_file_contents(file="input.txt"):
    """Read all lines from file."""
    with open(file) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    main()
