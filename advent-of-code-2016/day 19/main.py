"""Advent of Code 2016 Day 19."""


puzzle = 3017957


def main(number_elves=puzzle):
    circle_start, elves = get_elves_circle(number_elves)
    last_elf = steal_presents(circle_start)
    print(f'Elf with all presents: {last_elf}')
    circle_start, elves = get_elves_circle(number_elves)
    last_elf = steal_from_across(circle_start, elves, number_elves)
    print(f'Elf with all presents with stealing across: {last_elf}')


def steal_presents(circle_start):
    """Find last elf when stealing presents from next elf."""
    cur_elf = circle_start
    while cur_elf['next'] is not None:
        next_elf = cur_elf['next']
        if cur_elf is next_elf:
            break
        cur_elf = steal_from_next(cur_elf)
    return cur_elf['#']


def steal_from_next(elf):
    """Steal from next elf."""
    remove_elf(elf['next'])
    return elf['next']


def steal_from_across(circle_start, elves, number_elves):
    """Find last elf when stealing presents across."""
    cur_elf = circle_start
    middle = elves[number_elves // 2]
    for index in range(number_elves - 1):
        steal_from = middle
        remove_elf(steal_from)
        middle = middle['next']
        if (number_elves - index) % 2 != 0:
            middle = middle['next']
        cur_elf = cur_elf['next']
    return cur_elf['#']


def remove_elf(elf):
    """Remove elf from circle."""
    prev_elf = elf['prev']
    next_elf = elf['next']
    next_elf['prev'] = prev_elf
    prev_elf['next'] = next_elf


def get_elves_circle(number_elves):
    """Create circle with number_elves elves."""
    circle_start = None
    elves = []
    last_elf = None
    for elf in range(1, number_elves + 1):
        this_elf = {'#': elf, 'prev': None, 'next': None}
        elves.append(this_elf)
        if last_elf is None:
            circle_start = this_elf
        else:
            last_elf['next'] = this_elf
            this_elf['prev'] = last_elf
        last_elf = this_elf
    last_elf['next'] = circle_start
    circle_start['prev'] = last_elf
    return circle_start, elves


if __name__ == '__main__':
    main()
