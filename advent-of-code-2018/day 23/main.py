"""Advent of Code 2018 Day 23."""
import re


class Bot:
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def is_in_radius(self, x, y, z):
        return self.distance_to(x, y, z) <= self.radius

    def distance_to(self, x, y, z):
        pairs = [
            abs(val1 - val2)
            for val1, val2 in zip((x, y, z), (self.x, self.y, self.z))]
        return sum(pairs)

    @property
    def coordinates(self):
        return self.x, self.y, self.z

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z}), {self.radius}'


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    bots = parse_bots(lines)
    strongest_bot = find_strongest_bot(bots)
    bots_in_range = count_bots_in_range(bots, strongest_bot)
    print(f'Bots in range of radius of strongest bot: {bots_in_range}')
    best_position = find_best_position(bots)
    print('Shortest distance to point in range of most nanobots: '
          f'{sum(best_position)}')


def find_best_position(bots):
    """Find position in range of most bots and closest to (0, 0, 0)."""
    # Based on and inspired by reddit.
    xes, yes, zes = zip(*[bot.coordinates for bot in bots])
    ranges = [(min(vals), max(vals)) for vals in (xes, yes, zes)]
    grid_size = ranges[0][1] - ranges[0][0]
    ranges = [(minimum - grid_size, maximum + grid_size)
              for minimum, maximum in ranges]
    while grid_size > 0:
        x_vals, y_vals, z_vals = ranges
        max_count = 0
        best_grid = None
        best_distance = float('inf')
        for x in range(x_vals[0], x_vals[1] + 1, grid_size):
            for y in range(y_vals[0], y_vals[1] + 1, grid_size):
                for z in range(z_vals[0], z_vals[1] + 1, grid_size):
                    count = count_bots_on_grid(bots, x, y, z, grid_size)
                    distance = get_distance_to_0((x, y, z))
                    if max_count < count:
                        max_count = count
                        best_grid = [x, y, z]
                        best_distance = distance
                    elif max_count == count and best_distance > distance:
                        best_grid = [x, y, z]
                        best_distance = distance
        ranges = [(val - grid_size, val + grid_size) for val in best_grid]
        grid_size = grid_size // 2
    return best_grid


def count_bots_on_grid(bots, x, y, z, grid_size):
    """Count bots within the grid_size."""
    count = 0
    for bot in bots:
        cur_distance = bot.distance_to(x, y, z)
        if (cur_distance - bot.radius) // grid_size <= 0:
            count += 1
    return count


def get_distance_to_0(coordinates):
    """Get distance from (0, 0, 0) to coordinates."""
    return sum(abs(num) for num in coordinates)


def count_bots_in_range(bots, bot):
    """Count bots in range of bot."""
    counter = 0
    for other_bot in bots:
        if bot.is_in_radius(*other_bot.coordinates):
            counter += 1
    return counter


def find_strongest_bot(bots):
    """Find bot with largest radius."""
    return max(bots, key=lambda bot: bot.radius)


def parse_bots(lines):
    """Parse lines to bots."""
    bots = []
    for line in lines:
        bots.append(Bot(*[int(num) for num in re.findall(r'\-?\d+', line)]))
    return bots


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
