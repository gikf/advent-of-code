# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 09:01:29 2020
"""
from functools import lru_cache

WHITE = 0
BLACK = 1
DIRECTIONS = {
    'w': (-1, 1, 0),
    'e': (1, -1, 0),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
    'ne': (1, 0, -1),
    'sw': (-1, 0, 1),
}


def main():
    input_tiles = [line.strip() for line in get_file_contents()]
    tiles_to_flip = parse_tiles(input_tiles)
    initial_tiles, flipped_count = flip_initial_tiles(tiles_to_flip)
    print(f'Black tiles in the initial grid: {flipped_count}')
    after_100_days = pass_n_days(initial_tiles, 100)
    flipped_count_after_100_days = sum(
        value == BLACK for value in after_100_days.values()
    )
    print('Black tiles after similating 100 days: '
          f'{flipped_count_after_100_days}')


def pass_n_days(tiles, n):
    """Simulate passing n number of days, starting with initial tiles."""
    for _ in range(n):
        tiles = pass_day(tiles)
    return tiles


def pass_day(tiles):
    """Simulate single day.

    Rules:
        - Any black tile with zero or more than 2 black tiles
        immediately adjacent to it is flipped to white.
        - Any white tile with exactly 2 black tiles immediately
        adjacent to it is flipped to black.
    """
    next_day = tiles.copy()
    for coordinates, tile in tiles.items():
        neighbours = get_neighbours(coordinates)
        add_neighbours(coordinates, next_day)
        flipped_neighbours = count_flipped(neighbours, tiles)
        if is_flipped(tile):
            if flipped_neighbours == 0 or flipped_neighbours > 2:
                next_day[coordinates] = WHITE
        else:
            if flipped_neighbours == 2:
                next_day[coordinates] = BLACK
    return next_day


def flip_initial_tiles(directions):
    """Flip tiles represented found by directions in initial grid.

    Hexagonal grid is represented with cube coordinates.
    https://www.redblobgames.com/grids/hexagons/#coordinates-cube
    """
    tiles_in_grid = {}
    flipped_count = 0
    for tile_directions in directions:
        coordinates = [0, 0, 0]
        for direction in tile_directions:
            coordinates = [
                coord + coord_change
                for coord, coord_change in zip(
                    coordinates, DIRECTIONS[direction])
            ]
        final_coordinates = tuple(coordinates)
        tile = tiles_in_grid.get(final_coordinates, None)
        if tile:
            if is_flipped(tile):
                flipped_count -= 1
                tile_color = WHITE
            else:
                flipped_count += 1
                tile_color = BLACK
        else:
            tile_color = BLACK
            flipped_count += 1
            add_neighbours(final_coordinates, tiles_in_grid)
        tiles_in_grid[final_coordinates] = tile_color
    return tiles_in_grid, flipped_count


def add_neighbours(center_tile, tiles_in_grid):
    """Add missing neighours of the center_tile to the tiles_in_grid."""
    neighbours = get_neighbours(center_tile)
    for neighbour in neighbours:
        if neighbour not in tiles_in_grid:
            tiles_in_grid[neighbour] = WHITE


@lru_cache()
def get_neighbours(center_tile):
    """Get neighbours of center_tile, in accordance of cube coordinates."""
    return [
        tuple(
            coord + change
            for coord, change in zip(center_tile, direction))
        for direction in DIRECTIONS.values()
    ]


def count_flipped(tiles, grid):
    """Count number of flipped tiles from tiles list in grid."""
    return len([
        tile
        for tile in tiles
        if is_flipped(grid.get(tile, None))
    ])


def is_flipped(tile):
    """Check if tile is flipped."""
    return tile == BLACK


def parse_tiles(input_tiles):
    """Parse input_tiles to flip represented by str of directions."""
    tiles = []
    for tile in input_tiles:
        tiles.append(parse_directions(tile))
    return tiles


def parse_directions(input_directions):
    """Parse input_directions for single tile from str to list of str."""
    directions = []
    index = 0
    while index != len(input_directions):
        left = input_directions[index:]
        if left.startswith('s') or left.startswith('n'):
            directions.append(left[:2])
            index += 2
        else:
            directions.append(left[0])
            index += 1
    return directions


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
