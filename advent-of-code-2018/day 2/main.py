"""Advent of Code 2018 Day 2."""


def main(file_input='input.txt'):
    boxes = [line.strip() for line in get_file_contents(file_input)]
    checksum = get_checksum_for_boxes(boxes)
    print(f'Boxes checksum: {checksum}')
    common_letters = common_letters_in_IDs_differing_with_one_letter(boxes)
    print('Common letters between boxes differing with one letter: '
          f'{common_letters}')


def get_checksum_for_boxes(boxes):
    """Get checksum for boxes."""
    checksum = 1
    for count in (2, 3):
        checksum *= len([
            box for box in boxes if has_same_letter_repeated(box, count)
        ])
    return checksum


def common_letters_in_IDs_differing_with_one_letter(boxes):
    """Find common letters in two IDs, which are differing with one letter."""
    for index, box in enumerate(boxes[:-1]):
        for other_box in boxes[index + 1:]:
            same_letters = [letter_a
                            for letter_a, letter_b in zip(box, other_box)
                            if letter_a == letter_b]
            if len(box) - 1 == len(same_letters):
                return ''.join(same_letters)
    return None


def has_same_letter_repeated(box, times):
    """Check if box has any letter repeated number of times."""
    return any(
        box.count(letter) == times
        for letter in box
    )


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
