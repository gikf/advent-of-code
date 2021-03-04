"""Advent of Code 2017 Day 17."""

puzzle = 344
example = 3


def main(puzzle=puzzle):
    circular_buffer = create_buffer(get_node(0))
    value_after_2017 = insert_numbers(circular_buffer, puzzle)['next']['value']
    print(f'Value after 2017 value: {value_after_2017}')
    value_after_0 = find_value_after_0(puzzle, 50_000_000)
    print('Value after 0, after inserting 50,000,000 to '
          f'buffer: {value_after_0}')


def create_buffer(node):
    """Create circular buffer from node."""
    node['next'] = node
    node['prev'] = node
    return node


def find_value_after_0(steps, target):
    """Find value after 0 when target is inserted, with number steps each."""
    position = 0
    cur_value = 0
    for number in range(1, target + 1):
        position = (position + steps + 1) % number
        if position == 0:
            cur_value = number
    return cur_value


def insert_numbers(cur_element, steps, inserts=2017):
    """Insert inserts numbers into the buffer starting with cur_element.

    steps - number of steps to make forward in buffer to the position
        of next insertion.
    """
    for number in range(1, inserts + 1):
        for _ in range(steps):
            cur_element = cur_element['next']
        cur_element = insert_node_after(get_node(number), cur_element)
    return cur_element


def insert_node_after(new_node, insert_after):
    """Insert new_node into buffer after insert_after."""
    next_element = insert_after['next']
    next_element['prev'] = new_node
    new_node['next'] = insert_after['next']
    insert_after['next'] = new_node
    new_node['prev'] = insert_after
    return new_node


def get_node(value):
    """Return new node with value."""
    return {
        'value': value,
        'next': None,
        'prev': None,
    }


if __name__ == '__main__':
    main()
