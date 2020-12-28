# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 10:51:07 2020
"""
from collections import defaultdict, deque
import re


NEIGH = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
}

EDGE_TO_NEIGHBOUR = {
    'up': 2,
    'down': 3,
    'left': 0,
    'right': 1,
}


def main():
    input_squares = get_file_contents().split('\n\n')
    squares, square_to_edges, edge_to_squares = process_squares(
        parse_squares(input_squares)
    )

    corners = get_corners(square_to_edges, edge_to_squares)
    multiplied = 1
    for corner in corners:
        multiplied *= corner
    print(f'Multiplied corner ids: {multiplied}')

    grid = fill_grid(square_to_edges, edge_to_squares, corners)

    orientated_squares = orientate_grid(
        edge_to_squares, grid, square_to_edges, squares
    )
    image = get_image_from_squares(grid, orientated_squares)
    orientations = get_possible_orientations(image)
    for orientation in orientations:
        new_square, monsters_count = find_monsters(orientation)
        if monsters_count > 0:
            hashes = count_char_in_grid('#', orientation)
            hashes_after = count_char_in_grid('#', new_square)
            print(f'Monsters: {monsters_count}')
            print(f'# in total: {hashes}, left: {hashes_after}')


def count_char_in_grid(char, grid):
    """Count number of occurences of char in grid."""
    return sum(line.count(char) for line in grid)


def find_monsters(square):
    """Find monsters in square.

    Returns new square with selected monsters on grid and number of monsters
    found.
    """
    new_square = square[:]
    monster_ref = [
        r'                  # ',
        r'#    ##    ##    ###',
        r' #  #  #  #  #  #   ',
    ]
    monster = [
        r'[\.#]{18}#[\.#]{1}',
        r'#[\.#]{4}##[\.#]{4}##[\.#]{4}###',
        r'[\.#]{1}#[\.#]{2}#[\.#]{2}#[\.#]{2}#[\.#]{2}#[\.#]{2}#[\.#]{3}',
    ]
    monsters = 0
    for row_no, row in enumerate(square[:-2]):
        for col_no, col in enumerate(row[:-19]):
            if all(
                bool(re.findall(
                    regex, square[row_no + offset][col_no:col_no + 20]
                ))
                for offset, regex in enumerate(monster)
            ):
                for row_offset in range(3):
                    cur_row = row_no + row_offset
                    line = list(new_square[cur_row])
                    for col_offset, char in enumerate(monster_ref[row_offset]):
                        if char == '#':
                            cur_col = col_no + col_offset
                            line[cur_col] = 'O'
                    new_square[cur_row] = ''.join(line)
                monsters += 1
    return new_square, monsters


def lock_square(
        coordinates, edge_to_squares, grid, square_to_edges, squares):
    """Lock square in correct orientation."""
    row, column = coordinates
    square_id = grid[row][column]
    square = squares[square_id]
    orientations = get_possible_orientations(square)
    neighbours = get_neighbours_from_grid(row, column, grid)
    for orientation in orientations:
        cur_edges = get_edges(orientation)
        matching = 0
        for direction, neighbour in neighbours:
            neighbour_edges = square_to_edges[neighbour]
            relevant_edge = cur_edges[EDGE_TO_NEIGHBOUR[direction]]
            if any(relevant_edge in edge for edge in neighbour_edges):
                matching += 1
        if matching == len(neighbours):
            squares[square_id] = orientation
    return squares


def get_image_from_squares(grid, squares):
    """Join squares from the grid leaving out square borders to form image."""
    image = [
        '' for _ in range(8 * len(grid))
    ]
    for row_no, row in enumerate(grid):
        for col_no, square in enumerate(row):
            for square_line, line in enumerate(squares[square][1:-1]):
                image[row_no * 8 + square_line] += line[1:-1]
    return image


def orientate_grid(edge_to_squares, grid, square_to_edges, squares):
    """Orientate grid to match edges of each adjoin square."""
    for row_no, row in enumerate(grid):
        for col_no, col in enumerate(row):
            squares = lock_square(
                (row_no, col_no),
                edge_to_squares,
                grid,
                square_to_edges,
                squares
            )
    return squares


def get_corners(square_to_edges, edge_to_squares):
    """Get squares ids of squares which place in grid in corner."""
    return get_squares_with_free_edge(square_to_edges, edge_to_squares, 2)


def get_edge_squares(square_to_edges, edge_to_squares):
    """Get squares ids of squares which are placed on the edge of grid."""
    return get_squares_with_free_edge(square_to_edges, edge_to_squares, 1)


def get_squares_with_free_edge(
        square_to_edges, edge_to_squares, num_free_edges):
    """Get squares with num_free_edges number of edges that don't connect."""
    return [
        square
        for square in square_to_edges
        if sum(1 for edge in square_to_edges[square]
               if len(edge_to_squares[edge]) == 1
               ) == num_free_edges
    ]


def get_neighbours_from_grid(row, column, grid):
    """Get from the grid neighbours of square on given row and column."""
    coordinates = []
    if row > 0:
        coordinates.append(('up', row - 1, column))
    if row + 1 < len(grid):
        coordinates.append(('down', row + 1, column))
    if column > 0:
        coordinates.append(('left', row, column - 1))
    if column + 1 < len(grid):
        coordinates.append(('right', row, column + 1))
    return [
        (neighbour, grid[square_row][square_col])
        for neighbour, square_row, square_col in coordinates
    ]


def rotate_square_right(square):
    """Rotate square right by 90 degrees."""
    new_square = [
        [[] for _ in range(len(square))]
        for _ in range(len(square))
    ]
    for row, line in enumerate(square):
        for col, char in enumerate(line):
            new_square[col][len(square) - 1 - row] = char
    return [''.join(row) for row in new_square]


def flip_square(square, direction):
    """Flip square in left or up direction."""
    if direction == 'left':
        return [
            row[::-1] for row in square
        ]
    elif direction == 'up':
        return [
            row[:]
            for row in square[::-1]
        ]


def get_possible_orientations(square):
    """Get all possible orientations of square."""
    orientations = []
    cur_square = square
    for _ in range(4):
        cur_square = rotate_square_right(cur_square)
        orientations.append(cur_square)
        flipped = cur_square
        flipped = flip_square(flipped, 'left')
        orientations.append(flipped)
    return orientations


def fill_grid(
        square_to_edges,
        edge_to_squares,
        corners,
        grid=None,
        placed_squares=None):
    """Fill grid starting with one corner and then edges of the grid."""
    queue = deque()
    if grid is None:
        grid = create_grid(int(len(square_to_edges)**0.5))
        grid[0][0] = corners[0]
        start = corners[0]
        queue.extend(get_neighbour_squares(
            start, square_to_edges, edge_to_squares
        ))
        queue.extend(get_edge_squares(square_to_edges, edge_to_squares))
    else:
        grid = [row[:] for row in grid]
        for row in grid:
            for col in row:
                if col:
                    queue.extend(get_neighbour_squares(
                        col, square_to_edges, edge_to_squares
                    ))
    if placed_squares is None:
        placed_squares = {corners[0]: (0, 0)}
    else:
        placed_squares = placed_squares.copy()

    grid_size = len(grid), len(grid[0])
    times_square_visited = defaultdict(int)

    while queue and not is_grid_filled(grid):
        cur_square = queue.popleft()
        times_square_visited[cur_square] += 1
        if times_square_visited[cur_square] > 5:
            break
        if cur_square in placed_squares:
            continue

        possible_edges, square_edges = get_possible_edges(
            cur_square, square_to_edges, edge_to_squares, placed_squares
        )
        possible_squares = get_possible_positions(
            cur_square, possible_edges, square_edges, placed_squares, grid,
            grid_size
        )

        if len(possible_squares) == 1:
            (row, col), square = possible_squares[0]
            grid[row][col] = cur_square
            placed_squares[cur_square] = (row, col)
            queue.extend(get_neighbour_squares(
                cur_square, square_to_edges, edge_to_squares
            ))
        elif possible_squares:
            for option in possible_squares:
                (row, col), square = option
                grid[row][col] = square
                new_placed = placed_squares.copy()
                new_placed[square] = (row, col)
                result_grid = fill_grid(
                    square_to_edges, edge_to_squares, corners, grid, new_placed
                )
                if is_grid_filled(result_grid):
                    return result_grid
                    grid[row][col] = square
                    queue.extend(get_neighbour_squares(
                        square, square_to_edges, edge_to_squares))
                else:
                    grid[row][col] = []
    return grid


def get_possible_positions(
        square,
        possible_edges,
        square_edges,
        placed_squares,
        grid,
        grid_size):
    """Get currently possible positions for square."""
    possible_positions = []
    rows, cols = grid_size
    for _, cur_square in possible_edges:
        row, col = placed_squares[cur_square]
        if col + 1 == cols or grid[row][col + 1]:
            row += 1
        else:
            col += 1
        is_inside = is_square_inside(row, col, rows, cols)
        if len(square_edges) == 3 and is_inside:
            continue
        if len(square_edges) == 4 and not is_inside:
            continue
        if row >= rows or col >= cols:
            break
        possible_positions.append(((row, col), square))
    return possible_positions


def get_possible_edges(
        square, square_to_edges, edge_to_squares, placed_squares):
    """Get edges for square that are already placed."""
    possible_edges = []
    square_edges = []
    for cur_edge in square_to_edges[square]:
        squares_with_edge = edge_to_squares[cur_edge]
        if len(squares_with_edge) > 1:
            square_edges.append(squares_with_edge)
        for cur_square in squares_with_edge:
            if cur_square in placed_squares:
                possible_edges.append((cur_edge, cur_square))
    return possible_edges, square_edges


def is_square_inside(row, col, rows, cols):
    """Check if row and col is square inside grid having rows and cols."""
    return row not in (0, rows - 1) and col not in (0, cols - 1)


def is_grid_filled(grid):
    """Check if whole grid is filled."""
    return all(
        bool(square)
        for row in grid
        for square in row
    )


def get_neighbour_squares(square, square_to_edges, edge_to_squares):
    """Get squares that are neighbours - have one matching edge."""
    neighbour_squares = []
    for square_edge in square_to_edges[square]:
        squares_with_edge = edge_to_squares[square_edge]
        if len(squares_with_edge) > 1:
            neighbour_squares.extend([
                one_square for one_square in squares_with_edge
                if one_square != square
            ])
    return neighbour_squares


def process_squares(parsed_squares):
    """Process parsed_squares.

    Returns three dicts:
        - square_to_edges - dict mapping square id to list of edges of
            that square
        - edge_to_squares - dict mapping edge to list of squares having
            that edge
        - squares - dict mapping square id to representation of square."""
    square_to_edges = defaultdict(list)
    edge_to_squares = defaultdict(list)
    squares = {}
    for number, square in parsed_squares.items():
        cur_edges = [
            tuple(sorted([edge, edge[::-1]]))
            for edge in get_edges(square)]
        for edge in cur_edges:
            # print(edge)
            edge_to_squares[edge].append(number)
        square_to_edges[number] = cur_edges
        squares[number] = square
    return squares, square_to_edges, edge_to_squares


def get_edges(square):
    """Get edges of square."""
    left = right = ''
    for row in square:
        left += row[0]
        right += row[-1]
    return left, right, square[0], square[-1]


def create_grid(n):
    """Create grid having n rows and n columns."""
    return [
        [[] for _ in range(n)]
        for _ in range(n)
    ]


def parse_squares(input_squares):
    """Parse squares from the input_squares.

    Returns dict with keys being id of square and value list of str with
    square contents"""
    squares = {}
    for square in input_squares:
        if square:
            lines = [line.strip() for line in square.split('\n')]
            squares[int(lines[0].split()[1][:-1])] = [line.strip()
                                                      for line in lines[1:]]
    return squares


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
