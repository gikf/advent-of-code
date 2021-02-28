"""Advent of Code 2017 Day 13."""


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    layers = parse_layers(lines)
    positions = get_layer_positions(layers)
    severity = get_trip_severity(layers, positions[:])
    print(f'Severity of trip starting at picosecond 0: {severity}')
    delay = get_trip_delay(layers, positions[:])
    print(f'Picoseconds delay to not get caught: {delay}')


def get_trip_delay(layers, initial_positions):
    """Get delay needed for safe trip through layers."""
    cur_delay = 0
    positions = initial_positions[:]
    while will_be_caught(layers, positions):
        move_scanners(layers, positions)
        cur_delay += 1
    return cur_delay


def will_be_caught(layers, positions):
    """Check if you will be caught on any layer, based on initial positions."""
    for depth, params in layers.items():
        if (positions[depth] + depth) % params['range'] == 0:
            return True
    return False


def get_trip_severity(layers, positions):
    """Find severity of trip through layers, starting at positions."""
    last_layer = max(layers)
    severity = 0
    for layer in range(last_layer + 1):
        if is_caught(layers, positions, layer):
            severity += layer_severity(layers, layer)
        move_scanners(layers, positions)
    return severity


def get_layer_positions(layers):
    """Return list with initial layers positions."""
    return [0 if layer in layers else None
            for layer in range(max(layers) + 1)]


def is_caught(layers, positions, layer):
    """Check if you are caught on layer."""
    return layer in layers and positions[layer] == 0


def layer_severity(layers, layer):
    """Return severity of layer in layers."""
    return layers[layer]['severity']


def move_scanners(layers, positions):
    """Move scanner positions on layers."""
    for depth, params in layers.items():
        limit = params['range']
        position = positions[depth]
        positions[depth] = (position + 1) % limit
    return position


def parse_layers(lines):
    """Parse lines to layers, represented as dict of dicts."""
    layers = {}
    for line in lines:
        depth, range = parse_layer(line)
        layers[depth] = {
            'depth': depth,
            'range': (range - 1) * 2,
            'severity': depth * range
        }
    return layers


def parse_layer(line):
    """Parse line with layer data."""
    return [int(num) for num in line.split(': ')]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
