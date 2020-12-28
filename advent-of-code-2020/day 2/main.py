# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 13:11:13 2020
"""


def main():
    file_contents = get_file_contents()
    valid_passwords = validate_passwords(file_contents, validate_password)
    print(len(valid_passwords))
    valid_passwords_positions = validate_passwords(
        file_contents, validate_password_positions
    )
    print(len(valid_passwords_positions))


def validate_passwords(passwords, validator):
    """Validate passwords using validator.

    Returns list with valid passwords"""
    valid_passwords = []
    for entry in passwords:
        limit, chars, password = entry.split()
        nums = [int(num) - 1 for num in limit.split('-')]
        policy = (nums, chars[0])
        if validator(policy, password):
            valid_passwords.append(password)
    return valid_passwords


def validate_password(policy, password):
    """Validate password based on policy."""
    (minimum, maximum), char = policy
    count_char = password.count(char[0])
    return minimum <= count_char <= maximum


def validate_password_positions(policy, password):
    """Validate password based on positions in policy."""
    positions, char = policy
    password_chars = set(password[position] for position in positions)
    return len(password_chars) == 2 and char in password_chars


def get_file_contents(file="input.txt"):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == "__main__":
    main()
