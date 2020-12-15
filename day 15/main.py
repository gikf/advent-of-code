# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:01:05 2020
"""
from collections import defaultdict


NUMS = [0, 20, 7, 16, 1, 18, 15]


def main():
    print(say_number(NUMS, 30000000))


def say_number(starting_numbers, final_turn):
    """Number memory game."""
    turn = 0
    numbers = defaultdict(int)
    for number in starting_numbers:
        turn += 1
        numbers[number] = turn
        last_number = number
    while turn < final_turn:
        turn += 1
        if last_number not in numbers:
            next_number = 0
        else:
            next_number = turn - 1 - numbers[last_number]
        numbers[last_number] = turn - 1
        last_number = next_number
    return last_number


def say_number_slow(starting_numbers, final_turn):
    """Number memory game.

    Slower due to list appending of turns."""
    turn = 0
    numbers = defaultdict(list)
    for number in starting_numbers:
        turn += 1
        numbers[number].append(turn)
        last_number = number
    while turn < final_turn:
        turn += 1
        cur_number = numbers[last_number]
        try:
            next_number = cur_number[-1] - cur_number[-2]
        except IndexError:
            next_number = 0
        numbers[next_number].append(turn)
        last_number = next_number
    return last_number


if __name__ == '__main__':
    main()
