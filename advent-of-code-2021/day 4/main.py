"""Advent of Code 2021 Day 4."""
from typing import List


def main(file_input='input.txt'):
    bingo_numbers, boards = parse_bingo_input(get_file_contents(file_input))
    scores = score_boards(boards, bingo_numbers)
    first_winner_score, *_, last_winner_score = scores
    print(f'Score of first board to win: {first_winner_score}')
    print()
    print(f'Score of last board to win: {last_winner_score}')


def score_boards(boards, numbers, num_boards_to_score=None) -> List[int]:
    """Score num_boards_to_score boards, in order of finishing game."""
    if num_boards_to_score is None:
        num_boards_to_score = len(boards)

    scores = []
    for number in numbers:
        boards = [board for board in boards if not board.is_bingo()]
        for board in boards:
            board.mark(number)
            if board.is_bingo():
                scores.append(number * board.sum_unmarked())
            if len(scores) == num_boards_to_score:
                return scores
    return scores


def parse_bingo_input(lines):
    """Parse input lines to list of bingo numbers and list of boards."""
    numbers, *rest = [line.strip() for line in lines]
    bingo_numbers = [int(number) for number in numbers.split(',')]
    boards = parse_boards(rest)
    return bingo_numbers, boards


class Board:
    """Bingo board."""
    def __init__(self, numbers):
        self.numbers = [row[:] for row in numbers]
        self.marked = [
            [False for _ in numbers[0]]
            for _ in numbers
        ]

    def sum_unmarked(self):
        """Return sum of numbers unmarked on board."""
        return sum(
            number
            for row_no, row in enumerate(self.numbers)
            for col_no, number in enumerate(row)
            if not self.marked[row_no][col_no])

    def is_bingo(self):
        """Check if board finished game."""
        return (
            any(all(row) for row in self.marked)
            or any(
                all([row[column] for row in self.marked])
                for column, _ in enumerate(self.marked[0])
            )
        )

    def mark(self, wanted):
        """Mark wanted number on board."""
        for row_no, row in enumerate(self.numbers):
            for col_no, number in enumerate(row):
                if number != wanted:
                    continue
                self.marked[row_no][col_no] = True
                return True
        return False


def parse_boards(lines) -> List[Board]:
    """Parse lines with board rows to 5x5 boards."""
    boards = []
    cur_board = []
    for line in lines:
        if not line:
            continue
        numbers = [int(number) for number in line.split()]
        cur_board.append(numbers)
        if len(cur_board) == 5:
            boards.append(Board(cur_board))
            cur_board = []
    return boards


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
