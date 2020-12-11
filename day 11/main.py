# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:37:37 2020
"""


EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'

DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1)
]


def main():
    seats = [[*line.strip()] for line in get_file_contents()]
    filled_seats = take_seats(seats)
    print(count_occupied(filled_seats))
    truly_filled = take_first_seat(seats)
    print(count_occupied(truly_filled))


def take_seats(seats):
    """Find how seats will be occupied based on the standard seat rules.

    - If a seat is empty (L) and there are no occupied seats
      adjacent to it, the seat becomes occupied.
    - If a seat is occupied (#) and four or more seats adjacent
      to it are also occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.
    """
    max_row, max_column = len(seats) - 1, len(seats[0]) - 1
    while True:
        reference = copy_seats(seats)
        new_seats = copy_seats(seats)
        for row_no, row in enumerate(seats):
            for column_no, seat in enumerate(row):
                if seat == EMPTY:
                    adjacent_positions = get_adjacent_seat_positions(
                        row_no, column_no, max_row, max_column
                    )
                    if are_adjacent_empty(adjacent_positions, seats):
                        new_seats[row_no][column_no] = OCCUPIED
        seats = new_seats
        new_seats = copy_seats(seats)
        for row_no, row in enumerate(seats):
            for column_no, seat in enumerate(row):
                if seat == OCCUPIED:
                    adjacent_positions = get_adjacent_seat_positions(
                        row_no, column_no, max_row, max_column
                    )
                    if are_n_or_more_occupied(4, adjacent_positions, seats):
                        new_seats[row_no][column_no] = EMPTY
        if new_seats == reference:
            break
        seats = new_seats
    return new_seats


def take_first_seat(seats):
    """Find how seats will be occupied based on the first visible seat rules.

    - If a seat is empty (L) and there are no occupied first visible seats
      adjacent to it, the seat becomes occupied.
    - If a seat is occupied (#) and five or more first visible seats adjacent
      to it are also occupied, the seat becomes empty.
    - Otherwise, the seat's state does not change.
    """
    max_row, max_column = len(seats) - 1, len(seats[0]) - 1
    while True:
        reference = copy_seats(seats)
        for status, new_status, check in [
                (EMPTY, OCCUPIED, are_empty),
                (OCCUPIED, EMPTY, are_five_or_more_empty)
        ]:
            new_seats = copy_seats(seats)
            for row_no, row in enumerate(seats):
                for column_no, seat in enumerate(row):
                    if seat == status:
                        visible_adjacent_seats = get_visible_adjacent_seats(
                            row_no, column_no, seats, max_row, max_column
                        )
                        if check(visible_adjacent_seats):
                            new_seats[row_no][column_no] = new_status
            seats = new_seats
        if new_seats == reference:
            break
        seats = new_seats
    return new_seats


def are_empty(seats):
    """Check if there are no occupied seats."""
    return len(get_occupied(seats)) == 0


def are_five_or_more_empty(seats):
    """Check if there are five or more occupied seats."""
    return len(get_occupied(seats)) >= 5


def get_occupied(seats):
    """Get only occupied seats."""
    return [seat for seat in seats if seat == OCCUPIED]


def get_adjacent_seat_positions(row, column, max_row, max_column):
    """Get positions of the seats adjacent to the seat with row and column."""
    positions = []
    for cur_row in range(row - 1, row + 2):
        for cur_column in range(column - 1, column + 2):
            if cur_row == row and cur_column == column:
                continue
            if 0 <= cur_row <= max_row and 0 <= cur_column <= max_column:
                positions.append((cur_row, cur_column))
    return positions


def get_visible_adjacent_seats(row, column, seats, max_row, max_column):
    """Get first visible adjacent seats to the seat with row and column."""
    adjacent_seats = []
    for change_row, change_col in DIRECTIONS:
        cur_row, cur_column = row + change_row, column + change_col
        while 0 <= cur_row <= max_row and 0 <= cur_column <= max_column:
            cur_seat = seats[cur_row][cur_column]
            if not is_floor(cur_seat):
                adjacent_seats.append(cur_seat)
                break
            cur_row += change_row
            cur_column += change_col
    return adjacent_seats


def are_adjacent_empty(positions, seats):
    """Check if all seats from the positions are not OCCUPIED."""
    return all(
        seat != OCCUPIED
        for seat in get_seats(positions, seats)
    )


def is_floor(seat):
    """Check if seat is FLOOR."""
    return seat == FLOOR


def are_n_or_more_occupied(n, positions, seats):
    """Check if number of occupied seats on the positions is greater than n."""
    return len(
        [seat for seat in get_seats(positions, seats) if seat == OCCUPIED]
    ) >= n


def get_seats(positions, seats):
    """Get seats from positions list and seats list of lists."""
    return [seats[adj_row][adj_col] for adj_row, adj_col in positions]


def count_occupied(seats):
    """Count number of seats # in the seats."""
    return sum(row.count('#') for row in seats)


def copy_seats(seats):
    """Create copy of seats list of list."""
    return [[seat for seat in row] for row in seats]


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
