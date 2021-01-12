"""Advent of Code 2015 Day 16."""


mfcsam_print_out = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''.split('\n')


def main(file_input='input.txt'):
    lines = [line.strip() for line in get_file_contents(file_input)]
    wanted_properties = parse_properties(mfcsam_print_out)
    aunts = parse_aunts(lines)
    check_functions = {
        name: int.__eq__
        for name in wanted_properties
    }
    possible_aunts = find_aunt(aunts, wanted_properties, check_functions)
    print(possible_aunts)

    for properties, function in ((('cats', 'trees'), int.__lt__),
                                 (('pomeranians', 'goldfish'), int.__gt__)):
        for property_name in properties:
            check_functions[property_name] = function
    possible_stage2 = find_aunt(aunts, wanted_properties, check_functions)
    print(possible_stage2)


def find_aunt(aunts, properties, check_functions):
    """Find aunt(s) from aunts based on properties and check_functions."""
    possible_aunts = []
    for aunt, aunt_properties in aunts.items():
        if check_aunt(aunt_properties, properties, check_functions):
            possible_aunts.append(aunt)
    return possible_aunts


def check_aunt(aunt_properties, wanted_properties, check_functions):
    """Check if aunt_properties don't contradict wanted_properties."""
    for property_name, value in aunt_properties.items():
        check = check_functions[property_name]
        if not check(wanted_properties[property_name], value):
            return False
    return True


def parse_aunts(lines):
    """Parse aunts from lines."""
    return dict(parse_aunt(line) for line in lines)


def parse_aunt(line):
    """Parse line to tuple with name and dictionary of properties"""
    name, all_properties = line.split(': ', maxsplit=1)
    return name, parse_properties(all_properties.split(', '))


def parse_properties(properties):
    """Parse properties to dicionatry with property names and values."""
    parsed_properties = {}
    for one_property in properties:
        property_name, value = one_property.split(': ')
        parsed_properties[property_name] = int(value)
    return parsed_properties


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
