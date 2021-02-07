"""Advent of Code 2016 Day 17."""
from collections import deque
import hashlib
import re


puzzle = 'ioramepc'
MOVES = (
    ((-1, 0), 'U'),
    ((1, 0), 'D'),
    ((0, -1), 'L'),
    ((0, 1), 'R'),
)


def main(passcode=puzzle):
    grid = get_grid(4)
    shortest, *_, longest = sorted(find_paths(grid, passcode), key=len)
    print(f'Shortest path: {shortest}')
    print(f'Length of the longest path: {len(longest)}')


def find_paths(grid, passcode):
    """Find paths in grid depending on hashing passcode."""
    queue = deque([([(0, 0)], '')])
    target = (3, 3)
    paths = []
    while queue:
        positions, cur_path = queue.popleft()
        cur_position = positions[-1]
        if cur_position == target:
            paths.append(cur_path)
            continue
        next_moves = get_next_moves(
            grid, cur_position, get_hash(passcode, cur_path)[:4])
        for move, direction in next_moves:
            queue.append((positions + [move], cur_path + direction))
    return paths


def get_next_moves(grid, position, hash):
    """Get moves from position in grid, depending on hash."""
    moves = []
    for move, hash_char in zip(MOVES, hash):
        if not re.match(r'[b-f]', hash_char):
            continue
        row, col = position
        (row_change, col_change), direction = move
        next_row, next_col = row + row_change, col + col_change
        if (not is_in_limit(next_row, len(grid))
                or not is_in_limit(next_col, len(grid[0]))):
            continue
        moves.append(((next_row, next_col), direction))
    return moves


def is_in_limit(value, limit):
    """Check if value is within limit."""
    return 0 <= value < limit


def get_hash(passcode, path):
    """Get hash from passcode and path."""
    return hashlib.md5((passcode + path).encode()).hexdigest()


def get_grid(size):
    """Create grid with size."""
    return [[[] for _ in range(size)]
            for _ in range(size)]


if __name__ == '__main__':
    main()
