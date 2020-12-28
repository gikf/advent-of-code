# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 10:05:23 2020
"""


def main():
    input_data = [line.strip().split('\n')
                  for line in get_file_contents().split('\n\n')]
    (ranges, all_numbers,
     your_ticket, nearby_tickets) = parse_input_data(input_data)
    invalid_ticket_values = get_invalid_ticket_values(
        nearby_tickets, all_numbers
    )
    print(f'Ticket scanning error rate: {sum(invalid_ticket_values)}')
    valid_tickets = validate_tickets(nearby_tickets, all_numbers)
    fields_order = find_fields_order(ranges, [your_ticket] + valid_tickets)
    print(f'Fields order: {fields_order}')
    departure_info = get_departure_info(fields_order, your_ticket)
    print(f'Departure fields: {departure_info}')
    print(f'Multiplied departure fields: {product(departure_info)}')


def find_fields_order(ranges, tickets):
    """Find fields order for given tickets and ranges."""
    columns_number = len(tickets[0])
    rows = [(row_number, []) for row_number in range(columns_number)]
    row_sets = [
        set([row[column_number] for row in tickets])
        for column_number in range(columns_number)
    ]
    for row_index, row_set in enumerate(row_sets):
        for one_range in ranges:
            if len(row_set - one_range['numbers']) == 0:
                rows[row_index][1].append(one_range['name'])
    ordered_rows = sorted(rows, key=lambda item: len(item[1]))
    for row_number, row_names in ordered_rows:
        if len(rows[row_number][1]) == 1:
            for row_index, (cur_row_index, cur_row_names) in enumerate(rows):
                if row_number == row_index:
                    continue
                if row_names[0] in cur_row_names:
                    cur_row_names.remove(row_names[0])
                    rows[row_index] = (cur_row_index, cur_row_names)
    return [row[1][0] for row in rows]


def product(numbers):
    """Calculate product of multiplying numbers."""
    result = 1
    for number in numbers:
        result *= number
    return result


def get_departure_info(order, ticket):
    """Get numbers from ticket corresponding to departure fields from
    the fields order.
    """
    return [
        number
        for number, field_name in zip(ticket, order)
        if 'departure' in field_name
    ]


def parse_input_data(input_data):
    """Parse tickets data from the input_data."""
    ranges_data, your_ticket_data, tickets_data = input_data
    ranges, all_numbers = parse_range_data(ranges_data)
    your_ticket = parse_ticket(your_ticket_data[1])
    tickets = parse_tickets_data(tickets_data[1:])
    return ranges, all_numbers, your_ticket, tickets


def parse_range_data(range_data):
    """Parse rules of the tickets fields in range_data."""
    ranges = []
    all_numbers = set()
    for one_range in range_data:
        name, two_ranges = one_range.split(':')
        allowed_numbers = set()
        for start_end in two_ranges.split(' or '):
            start, end = [int(num) for num in start_end.split('-')]
            allowed_numbers = allowed_numbers | set(range(start, end + 1))
        ranges.append({
            'name': name,
            'numbers': allowed_numbers
        })
        all_numbers = all_numbers | allowed_numbers
    return ranges, all_numbers


def validate_tickets(tickets, allowed_numbers):
    """Validate tickets with alllowed_numbers."""
    return [
        ticket
        for ticket in tickets
        if is_valid_ticket(ticket, allowed_numbers)
    ]


def is_valid_ticket(ticket, allowed_numbers):
    """Check if ticket is valid - all ticket numbers are in allowed_numbers."""
    return len(set(ticket) - allowed_numbers) == 0


def get_invalid_ticket_values(tickets, allowed_numbers):
    """Get values from tickets not matching any number in allowed_numbers."""
    invalid = []
    for ticket in tickets:
        ticket_set = set(ticket) - allowed_numbers
        if ticket_set:
            invalid.append(*ticket_set)
    return invalid


def parse_tickets_data(tickets_data):
    """Parse tickets from tickets_data"""
    return [
        parse_ticket(ticket) for ticket in tickets_data
    ]


def parse_ticket(ticket_data):
    """Parse str ticket_data to list of int"""
    return [int(num) for num in ticket_data.split(',')]


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
