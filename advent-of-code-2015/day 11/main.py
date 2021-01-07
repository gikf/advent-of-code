"""Advent of Code 2015 Day 11."""

puzzle = 'vzbxkghb'


def main():
    validators = (
        (lambda text, param: not does_include(text, param), 'iol'),
        (has_n_letter_pairs, 2),
        (has_increasing_straight_length, 3)
    )
    password = puzzle
    for _ in range(2):
        password = find_next_password(password, validators)
        print(password)


def find_next_password(cur_password, validators):
    """Find next password after cur_password, fulfilling validators.

    :param validators: Validators required to pass from new password.
    :type validators: List of tuples with function and parameter.
    """
    while True:
        cur_password = increment_password(cur_password)
        if validate_password(cur_password, validators):
            return cur_password


def increment_password(password):
    """Increment password by one.

    Starting from the right increase by one letter, if it was 'z',
    wrap it to 'a' and increment next letter to the left, until letter
    doesn't wrap

    Examples:
    xx -> xy
    xy -> xz
    xz -> ya
    ya -> yb
    """
    start, end = ord('a'), ord('z')
    codes = get_char_codes(password)
    codes[-1] += 1
    for index, code in enumerate(codes[::-1]):
        if code <= end:
            break
        code = start
        codes[-1 - index] = code
        codes[-2 - index] += 1
    return ''.join(chr(code) for code in codes)


def validate_password(password, validators):
    """Validate password with all validators."""
    return all(
        validator(password, parameter) for validator, parameter in validators)


def does_include(text, chars):
    """Check if text contains any character from chars."""
    return any(char in text for char in chars)


def has_n_letter_pairs(text, number):
    """Check if text has number of repeating adjoin letters."""
    pairs = 0
    prev_pair = None
    for index, letter in enumerate(text[1:]):
        if letter == text[index] and prev_pair != index:
            pairs += 1
            prev_pair = index + 1
    return pairs >= number


def has_increasing_straight_length(text, straight_length):
    """Check if text contain increasing straight of straight_length.

    Examples of length 3: abc, bcd, cde, xyz.
    """
    longest = 0
    codes = get_char_codes(text)
    cur_length = 1
    for index, code in enumerate(codes[1:]):
        if code - 1 == codes[index]:
            cur_length += 1
        else:
            if longest < cur_length:
                longest = cur_length
            cur_length = 1
    return longest >= straight_length


def get_char_codes(text):
    """Change text to list of character codes of the characters."""
    return [ord(letter) for letter in text]


if __name__ == '__main__':
    main()
