"""Advent of Code 2015 Day 20."""
from collections import defaultdict

puzzle = 33100000


def main(puzzle=puzzle):
    lowest_house = find_lowest_house_over(wanted_presents=puzzle,
                                          presents_mult=10)
    print(f'Lowest house number with presents over {puzzle}: {lowest_house}')
    lowest_house2 = find_lowest_house_over(wanted_presents=puzzle,
                                           presents_mult=11,
                                           houses_per_elf=50)
    print(f'Lowest house number with presents over {puzzle}, '
          f'with houses limit per elf: {lowest_house2}')


def find_lowest_house_over(wanted_presents,
                           presents_mult, houses_per_elf=None):
    """Find lowest house number with presents over wanted_presents.

    Each elf is numbered and delivers his number multiplied by
    presents_mult to houses_per_elf houses.
    """
    houses = defaultdict(int)
    elf_limit = wanted_presents // 10
    elf_number = 1
    lowest_house = float('inf')
    while elf_number <= elf_limit and elf_number <= lowest_house:
        presents_to_deliver = elf_number * presents_mult
        house_number = elf_number
        house_count = 0
        while house_number <= elf_limit and houses_per_elf != house_count:
            houses[house_number] += presents_to_deliver
            if houses[house_number] >= wanted_presents:
                lowest_house = min(house_number, lowest_house)
            house_number += elf_number
            house_count += 1
        elf_number += 1
    return lowest_house


if __name__ == '__main__':
    main()
