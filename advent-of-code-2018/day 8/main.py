"""Advent of Code 2018 Day 8."""


def main(file_input='input.txt'):
    numbers = [int(num)
               for num in get_file_contents(file_input)[0].strip().split()]
    tree, _ = parse_tree(numbers)
    print(f'Sum of all metadata entries: {sum_metadata(tree)}')
    print(f'Value of root node: {root_value(tree)}')


def parse_tree(numbers):
    """Parse numbers to tree.

    Tree is made up of nodes, node consists of:
    - number of child nodes
    - number of metadata entries
    - zero or more child nodes
    - one or more metadata entries."""
    tree = {'children': []}
    children_count, metadata_count, *numbers = numbers
    for _ in range(children_count):
        children_tree, numbers = parse_tree(numbers)
        tree['children'].append(children_tree)
    tree['metadata'] = numbers[:metadata_count]
    return tree, numbers[metadata_count:]


def root_value(tree):
    """Return value of the root node of tree.

    If node doesn't have children value is sum of its metadata.
    Otherwise metadata entries are 1-indexed references to child nodes."""
    if not tree['children']:
        return sum_metadata(tree)
    return sum(
        root_value(tree['children'][child_index - 1])
        for child_index in tree['metadata']
        if 1 <= child_index <= len(tree['children']))


def sum_metadata(tree):
    """Sum metadata values in tree."""
    return (sum(tree['metadata'])
            + sum([sum_metadata(child) for child in tree['children']]))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
