# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 11:29:57 2020
"""

import re


def main():
    file_contents = get_file_contents()
    passports = parse_passports(file_contents)
    valid_passports = validate_passports(passports)
    print(len(passports))
    print(f'Valid passports: {len(valid_passports)}')


def parse_passports(file_contents):
    passports = []
    cur_passport = []
    for passport_data in file_contents.split('\n'):
        if not passport_data:
            passport = parse_passport(' '.join(cur_passport))
            passports.append(passport)
            cur_passport = []
        else:
            cur_passport.append(passport_data)
    return passports


def parse_passport(passport):
    parsed_passport = {}
    for pair in passport.split():
        key, value = pair.split(':')
        parsed_passport[key] = value
    return parsed_passport


def validate_passports(passports):
    valid_passports = []
    for passport in passports:
        if validate_passport(passport):
            valid_passports.append(passport)
    return valid_passports


def validate_passport(passport):
    required_fields = [
        ('byr', validate_byr),
        ('iyr', validate_iyr),
        ('eyr', validate_eyr),
        ('hgt', validate_hgt),
        ('hcl', validate_hcl),
        ('ecl', validate_ecl),
        ('pid', validate_pid)
    ]
    for field, validator in required_fields:
        if field not in passport or not validator(passport[field]):
            print(field, passport)
            return False
    return True


def validate_byr(byr):
    return validate_year(byr, 1920, 2002)


def validate_iyr(iyr):
    return validate_year(iyr, 2010, 2020)


def validate_eyr(eyr):
    return validate_year(eyr, 2020, 2030)


def validate_hgt(hgt):
    if hgt.endswith('cm'):
        return 150 <= int(hgt[:-2]) <= 193
    elif hgt.endswith('in'):
        return 59 <= int(hgt[:-2]) <= 76
    return False


def validate_hcl(hcl):
    return bool(re.match(r'^#[0-9a-f]{6}$', hcl))


def validate_ecl(ecl):
    return ecl in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')


def validate_pid(pid):
    return len(pid) == 9 and pid.isdigit()


def validate_year(year, minimum, maximum):
    return len(year) == 4 and minimum <= int(year) <= maximum


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
