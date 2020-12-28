# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:29:38 2020
"""


def main():
    tree_map = get_file_contents()
    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    tree_counts = [
        count_trees(tree_map, down, right)
        for down, right in slopes
    ]
    print(tree_counts)
    print(product(tree_counts))


def product(numbers):
    """Multiply together numbers."""
    result = 1
    for number in numbers:
        result *= number
    return result


def count_trees(tree_map, down, right):
    """Count number of trees encountered in tree_map, with down, right steps."""
    column = 0
    trees = 0
    for index, row in enumerate(tree_map[::down]):
        if row[column] == '#':
            trees += 1
        column = (column + right) % len(row)
    return trees


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    main()
