"""Advent of Code 2017 Day 4."""


def main(file_input='input.txt'):
    passphrases = [line.strip().split()
                   for line in get_file_contents(file_input)]
    validators = (
        ('no duplicates', no_duplicates),
        ('no anagrams', no_anagrams),
    )
    for description, validator in validators:
        valid_passphrases = validate_passphrases(passphrases, validator)
        print(f'Valid passphrases with rule {description}: '
              f'{len(valid_passphrases)}')


def validate_passphrases(passphrases, validator):
    """Validate passphrases with validator function."""
    return [passphrase for passphrase in passphrases
            if validator(passphrase)]


def no_anagrams(passphrase):
    """Checks if passphrase doesn't contain words that are anagrams."""
    anagrams = set(''.join(sorted(word)) for word in passphrase)
    return len(passphrase) == len(anagrams)


def no_duplicates(passphrase):
    """Checks if passphrase doesn't contain duplicated words."""
    return len(passphrase) == len(set(passphrase))


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
