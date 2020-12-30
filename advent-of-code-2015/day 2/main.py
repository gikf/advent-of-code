"""Advent of Code Day 2."""


def main(input_file='input.txt'):
    presents = parse_presents(
        line.strip() for line in get_file_contents(input_file))
    needed_paper = count_needed_for_presents(presents, count_paper)
    print(f'Needed paper: {needed_paper}')
    needed_ribbon = count_needed_for_presents(presents, count_ribbon)
    print(f'Needed ribbon: {needed_ribbon}')


def count_needed_for_presents(presents, counter):
    """Calculate needed resource needed for presents using counter function."""
    return sum(
        counter(present)
        for present in presents
    )


def count_ribbon(present):
    """Calculate needed ribbon for present.

    Nedded ribbon is smallest perimeter of any present face,
    added to volume of the present.
    """
    counted_perimeters = sum(sorted(get_sides_doubled(present))[:2])
    return counted_perimeters + get_present_volume(present)


def get_sides_doubled(present):
    """Calculate doubled length of each side of the present."""
    return [
        side * 2 for side in present
    ]


def get_present_volume(present):
    """Calculate volume of the box needed for present."""
    volume = 1
    for side in present:
        volume *= side
    return volume


def count_paper(present):
    """Calculate needed paper.

    paper needed is area of the box:
        2*l*w + 2*w*h + 2*h*l
    and added smallest of the sides area
    """
    l, w, h = present
    side_areas = [
        get_area(edge_a, edge_b)
        for edge_a, edge_b in ((l, w), (w, h), (h, l))
    ]
    return sum(2 * side for side in side_areas) + min(side_areas)


def get_area(a, b):
    """Calculate area of rectangle with sides a and b."""
    return a * b


def parse_presents(lines):
    """Parse presents from list of str."""
    return [
        parse_present(present) for present in lines
    ]


def parse_present(present):
    """Parse present from axbxc to list of int."""
    return [int(num) for num in present.split('x')]


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
