"""Advent of Code 2016 Day 13."""
from collections import deque


WALL = '#'
EMPTY = '.'
MOVES = (
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
)
puzzle = 1352


def main(fav_number=puzzle):
    grid = create_grid(51)
    maze = draw_maze(grid, fav_number)
    fewest_steps = find_fewest_steps_to(maze, (1, 1), (39, 31))
    print(f'Fewest steps to reach (39, 31): {fewest_steps}')
    visited_positions_in_50_steps = find_unique_positions_in_steps(
        maze, (1, 1), 50)
    print('Unique positions visited in 50 steps: '
          f'{visited_positions_in_50_steps}')


def find_fewest_steps_to(maze, source, target):
    """Find fewest steps needed in maze to reach target from source."""
    path, _ = find_path(maze, source, did_reach(target))
    if path:
        return len(path) - 1
    return None


def find_unique_positions_in_steps(maze, source, steps):
    """Find number of unique positions visited in maze from source in steps."""
    _, visited = find_path(maze, source, steps_limit(steps))
    return len(visited)


def find_path(maze, source, target_check):
    """Find path on maze starting from source, with target_check condition."""
    visited = set()
    queue = deque([[source]])
    while queue:
        cur_path = queue.popleft()
        last_position = cur_path[-1]
        if target_check(cur_path):
            return cur_path, visited
        if last_position in visited:
            continue
        visited.add(last_position)
        for move in get_moves(maze, last_position):
            next_path = cur_path + [move]
            queue.append(next_path)
    return None, None


def did_reach(target):
    """Wrapper function to check if last move in path is target."""
    def wrapper(path):
        if path[-1] == target:
            return True
        return False
    return wrapper


def steps_limit(limit):
    """Wrapper function to check if path made limit steps."""
    def wrapper(path):
        if len(path) - 1 == limit + 1:
            return True
        return False
    return wrapper


def get_moves(maze, position):
    """Get possible moves in maze from position."""
    row, column = position
    moves = []
    for row_change, column_change in MOVES:
        new_row, new_column = row + row_change, column + column_change
        if (not is_in_limit(new_row, len(maze))
                or not is_in_limit(new_column, len(maze[0]))):
            continue
        if is_empty(maze[new_row][new_column]):
            moves.append((new_row, new_column))
    return moves


def is_in_limit(value, limit):
    """Check if value is within limit."""
    return 0 <= value < limit


def is_empty(position_symbol):
    """Check if position_symbol represents EMPTY"""
    return position_symbol == EMPTY


def draw_maze(grid, fav_number):
    """Draw maze on grid, using fav_number to calculate symbols."""
    maze = [row[:] for row in grid]
    for row_no, row in enumerate(grid):
        for col_no, column in enumerate(row):
            maze[row_no][col_no] = draw_coordinate(row_no, col_no, fav_number)
    return maze


def draw_coordinate(row, col, fav_number):
    """Get symbol for row and col, depending on fav_number.


    Symbol determination:
    - Find x*x + 3*x + 2*x*y + y + y*y.
    - Add the office designer's favourite number.
    - Find the binary representation of that sum;
        count the number of bits that are 1.
    - If the number of bits that are 1 is even, it's an open space.
    - If the number of bits that are 1 is odd, it's a wall.
    """
    coordinate_sum = col * col + 3 * col + 2 * col * row + row + row * row
    binary = bin(coordinate_sum + fav_number)
    number_of_bits_1 = sum(bit == '1' for bit in binary)
    return EMPTY if number_of_bits_1 % 2 == 0 else WALL


def create_grid(size):
    """Create grid of size filled with EMPTY."""
    return [[EMPTY for _ in range(size)] for _ in range(size)]


if __name__ == '__main__':
    main()
