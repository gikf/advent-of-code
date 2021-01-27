"""Advent of Code 2016 Day 6."""
from collections import defaultdict


def main(file_input='input.txt'):
    messages = [line.strip() for line in get_file_contents(file_input)]
    corrected_message = error_correct(messages, get_most_common)
    print(corrected_message)
    modified_corrected = error_correct(messages, get_least_common)
    print(modified_corrected)


def error_correct(messages, frequency):
    """Get error corrected message from messages, using frequency function."""
    message_length = len(messages[0])
    counted = {number: defaultdict(int)
               for number in range(message_length)}
    for message in messages:
        for index, char in enumerate(message):
            counted[index][char] += 1
    corrected_message = frequency(counted, message_length)
    return corrected_message


def get_common(counted, message_length, reverse):
    """Get most common letters from counted one letter per counted index."""
    message = []
    for index in range(message_length):
        message.append(sorted(
            counted[index],
            key=counted[index].__getitem__,
            reverse=reverse)[0])
    return ''.join(message)


def get_most_common(*args, **kwargs):
    """Call get_common with argument finding most common letters."""
    return get_common(*args, **kwargs, reverse=True)


def get_least_common(*args, **kwargs):
    """Call get_common with argument finding least common letters."""
    return get_common(*args, **kwargs, reverse=False)


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
