# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 09:35:44 2020
"""

puzzle_input = '538914762'
example = '389125467'


def main():
    puzzle = parse_puzzle(puzzle_input, 9)
    hundred_rounds = play_cups(puzzle, 100)
    print(f'Hundred rounds: {result(hundred_rounds)}')
    puzzle = parse_puzzle(puzzle_input)
    ten_millions = play_cups(puzzle, 10**7)
    star = ten_millions[1]
    star2 = ten_millions[star]
    print('Stars hidden behind:', star, star2)
    print(f'Multiplied: {star * star2}')


def play_cups(puzzle, moves_num):
    """Play moves_num number of rounds, with puzzle."""
    start = puzzle[0]
    puzzle_size = len(puzzle)
    for round_no in range(moves_num):
        puzzle, start = move(puzzle, start, puzzle_size)
    return puzzle


def move(puzzle, start_value, maximum=10):
    """Play single move with puzzle, using start_value."""
    picks = []
    start = puzzle[start_value]
    end = start
    while len(picks) != 3:
        picks.append(end)
        end = puzzle[end]
    puzzle[start_value] = end
    destination = start_value - 1
    while destination < 1 or destination in picks:
        destination = (destination - 1) % maximum
    puzzle[destination], puzzle[picks[2]] = (
        picks[0], puzzle[destination]
    )
    return puzzle, end


def result(puzzle):
    """Format puzzle to result."""
    result = []
    start = 1
    next_number = puzzle[start]
    while next_number != 1:
        result.append(next_number)
        next_number = puzzle[next_number]
    return ''.join(str(num) for num in result)


def parse_puzzle(puzzle, maximum=10**6):
    """Parse input puzzle, with maximum number of numbers in puzzle."""
    parsed_puzzle = [None for _ in range(maximum + 1)]
    initial_puzzle = parse_numbers(puzzle)
    for prev_index, number in enumerate(initial_puzzle[1:]):
        parsed_puzzle[initial_puzzle[prev_index]] = number
    last_number = initial_puzzle[-1]
    for number in range(max(initial_puzzle) + 1, maximum + 1):
        parsed_puzzle[last_number] = number
        last_number = number
    parsed_puzzle[last_number] = initial_puzzle[0]
    parsed_puzzle[0] = initial_puzzle[0]
    return parsed_puzzle


def parse_numbers(numbers):
    """Return list of numbers."""
    return [int(number) for number in numbers]


if __name__ == '__main__':
    main()
