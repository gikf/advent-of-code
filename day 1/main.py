# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 08:14:17 2020
"""

from data import numbers


def summing_numbers(target, nums):
    """Find target sum from two numbers in nums."""
    for index, num1 in enumerate(nums):
        for num2 in nums[index + 1:]:
            if num1 + num2 == target:
                return num1, num2


def sum_n_numbers(target, nums, n):
    """Find target sum from n numbers in nums."""
    sums = {num: [num] for num in nums}
    for iteration in range(n - 1):
        for num in nums:
            updates = {}
            for cur_num, sum_from in sums.items():
                # print(cur_num, sum_from)
                if num in sum_from:
                    continue
                if iteration + 1 != len(sum_from):
                    continue
                cur_sum = num + sum(sum_from)
                if cur_sum <= target:
                    cur_from = sum_from[:]
                    cur_from.append(num)
                    updates[cur_sum] = cur_from
            sums.update(updates)
    return sums.get(target)


def multi(numbers):
    product = 1
    for number in numbers:
        product *= number
    return product


def main():
    target = 2020
    nums = summing_numbers(target, numbers)
    print(f'Numbers summing to {target}: {[*nums]}')
    print(f'Numbers multiplicated: {multi(nums)}')
    n = 3
    nums = sum_n_numbers(target, numbers, 3)
    print(f'{n} numbers summing to {target}: {[*nums]}')
    print(f'Numbers multiplicated: {multi(nums)}')


if __name__ == '__main__':
    main()
