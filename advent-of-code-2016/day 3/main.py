"""Advent of Code 2016 Day 3."""


def main(file_input='input.txt'):
    triangles = [[int(side) for side in line.strip().split()]
                 for line in get_file_contents(file_input)]
    possible_triangles = get_possible_triangles(triangles)
    print(f'Number of possible triangles: {len(possible_triangles)}')
    column_triangles = parse_triangles(triangles)
    possible_column_triangles = get_possible_triangles(column_triangles)
    print('Number of possible triangles when triangles are in columns '
          f'in input: {len(possible_column_triangles)}')


def get_possible_triangles(triangles):
    """Get all possible triangles."""
    return [triangle
            for triangle in triangles
            if is_triangle_possible(triangle)]


def is_triangle_possible(triangle):
    """Check if triangle is possible."""
    return sum(sorted(triangle)[:2]) > max(triangle)


def parse_triangles(lines):
    """Parse triangles from three numbers in the same column."""
    triangles = []
    for index, _ in enumerate(lines[::3]):
        row_index = 3 * index
        cur_triangles = [[] for _ in range(3)]
        for row in range(3):
            for column in range(3):
                cur_triangles[column].append(lines[row_index + row][column])
        triangles.extend(cur_triangles)
    return triangles


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
