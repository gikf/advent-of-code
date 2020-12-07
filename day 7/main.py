# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 12:50:29 2020
"""
from collections import defaultdict


def main():
    lines = [line.strip() for line in get_file_contents()]
    rules = parse_rules(lines)
    bag_to_outer_bag = get_containers(rules)
    print(rules['faded teal'])
    print(count_bags_having('shiny gold', bag_to_outer_bag, set()))
    print(count_bags_inside('shiny gold', rules))


def parse_rules(lines):
    """Parse lines with rules."""
    rules = {}
    for line in lines:
        outer_bag_name, contents = line.split(' bags contain ')
        rules[outer_bag_name] = {}
        if 'no other bags.' in contents:
            continue
        for content in contents.split(','):
            number, inside = content.split(maxsplit=1)
            inside_bag = ' '.join(inside.split()[:-1])
            rules[outer_bag_name][inside_bag] = int(number)
    return rules


def get_containers(rules):
    """Invert rules dictionary to bag_inside: [outside_bag1, outside_bag2]."""
    bag_to_outer_bag = defaultdict(list)
    for outer_bag, contents in rules.items():
        for inside_bag in contents:
            bag_to_outer_bag[inside_bag].append(outer_bag)
    return bag_to_outer_bag


def count_bags_having(bag_name, bag_to_outer_bag, visited):
    """Count number of bags containing bag_name."""
    if bag_name in visited:
        return 0
    count = 0
    for bag in bag_to_outer_bag[bag_name]:
        if bag in visited:
            continue
        count += 1 + count_bags_having(bag, bag_to_outer_bag, visited)
        visited.add(bag)
    return count


def count_bags_inside(bag_name, rules):
    """Count total number of bags in bag_name."""
    if not rules[bag_name]:
        return 0
    count = 0
    for inside_bag, number_of_bags in rules[bag_name].items():
        count += (number_of_bags + number_of_bags
                  * count_bags_inside(inside_bag, rules))
    return count


def get_file_contents(file="input.txt"):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
