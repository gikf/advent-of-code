"""Advent of Code 2019 Day 8."""


COLORS = {
    '0': ' ',
    '1': '#',
}
TRANSPARENT = '2'


def main(file_input='input.txt'):
    data = get_file_contents(file_input)[0].strip()
    image_size = 6, 25
    layers = parse_data(data, image_size)
    layer_with_fewest_zeros = sorted(
        layers,
        key=lambda layer: count_in_layer(layer, '0'))[0]
    ones, twos = [
        count_in_layer(layer_with_fewest_zeros, num) for num in ('1', '2')]
    print('Number of 1 digits multiplied by number of 2 digits, in layer '
          f'having fewest 0 digits: {ones * twos}')
    print()
    image = decode_image(layers, image_size)
    print('Message:')
    for row in image:
        print(''.join(row))


def decode_image(layers, image_size):
    """Decode image of image_size from layers."""
    rows, columns = image_size
    image = []
    for row in range(rows):
        image.append([])
        for column in range(columns):
            for layer in layers:
                cur_pixel = layer[row][column]
                if cur_pixel == TRANSPARENT:
                    continue
                image[row].append(COLORS[cur_pixel])
                break
    return image


def count_in_layer(layer, number):
    """Count occurrences of number in layer."""
    return sum(row.count(number) for row in layer)


def parse_data(data, image_size):
    """Parse data to layers of image_size."""
    rows, columns = image_size
    layers = []
    layers_number = int(len(data) / (rows * columns))
    for index in range(layers_number):
        cur_layer = []
        for row in range(rows):
            start = (row + index * rows) * columns
            end = start + columns
            cur_layer.append(data[start:end])
        layers.append(cur_layer)
    return layers


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
