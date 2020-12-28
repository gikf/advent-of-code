# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:33:56 2020
"""

from collections import defaultdict


def main():
    adapters = sorted([int(adapter) for adapter in get_file_contents()])
    adapters = [0] + adapters + [max(adapters) + 3]
    joltage_differences = get_differences(adapters)
    print(joltage_differences[1] * joltage_differences[3])
    combinations = count_combinations(0, adapters)
    print(combinations)


def count_combinations(start_index, numbers, memo={}):
    """Count number of ways numbers can be ararnged.

    difference of adjoin arranged numbers can't be higher than 3."""
    if start_index in memo:
        return memo[start_index]
    if start_index + 1 == len(numbers):
        return 1

    count = 0
    cur_jolt = numbers[start_index]
    for index in range(start_index + 1, start_index + 4):
        if index < len(numbers):
            next_jolt = numbers[index]
            if cur_jolt + 3 >= next_jolt:
                count += count_combinations(index, numbers)
    memo[start_index] = count
    return count


def get_differences(numbers):
    """Get counts of differences between adjoin numbers."""
    differences = defaultdict(int)
    prev = numbers[0]
    for number in numbers[1:]:
        difference = number - prev
        differences[difference] += 1
        prev = number
    return differences


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
