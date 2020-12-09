# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 18:53:47 2020
"""


def main():
    numbers = [int(num.strip()) for num in get_file_contents()]
    for start_index, one_sum in enumerate(numbers[25:]):
        if not is_sum_of(one_sum, numbers[start_index:start_index + 25]):
            print(one_sum, numbers[start_index:start_index + 25])
            break
    n = 32321523
    print(f'Looknig for {n}')
    summing_set = get_set_summing_to(n, numbers)
    print(summing_set)
    minimum, maximum = min(summing_set), max(summing_set)
    print(f'Minimum: {minimum}, maximum: {maximum}, sum: {minimum + maximum}')


def is_sum_of(target, numbers):
    """Find if target number can be summed from two numbers."""
    for index, number in enumerate(numbers):
        new_target = target - number
        if new_target in set(numbers[0:index] + numbers[index:]):
            return True
    return False


def get_set_summing_to(target, numbers):
    """Get continous set of numbers summing up to target."""
    left = 0
    right = 0
    cur_sum = 0
    while cur_sum != target:
        if cur_sum < target:
            cur_sum += numbers[right]
            right += 1
        elif cur_sum > target:
            cur_sum -= numbers[left]
            left += 1
    return numbers[left:right]


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
