"""Advent of Code 2015 Day 1"""

def main(input_file='input.txt'):
    directions = [line.strip() for line in get_file_contents(input_file)][0]
    final_floor = count_char('(', directions) - count_char(')', directions)
    print(f'Final floor: {final_floor}')
    basement_enter_position = find_when_entered_basement(directions)
    print(f'Entered basement at position: {basement_enter_position}')


def find_when_entered_basement(text):
    """Find position in text when santa enters basement first time."""
    cur_floor = 0
    for position, floor_change in enumerate(text, start=1):
        cur_floor += 1 if floor_change == '(' else -1
        if cur_floor < 0:
            return position
    return -1


def count_char(char, text):
    """Count number of occurences of char in text."""
    return text.count(char)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
