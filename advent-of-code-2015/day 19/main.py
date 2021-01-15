"""Advent of Code 2015 Day 19."""
from collections import defaultdict
import random


def main(file_input='input.txt'):
    lines, molecule = [part.strip()
                       for part in get_file_contents(file_input).split('\n\n')]
    rules = parse_rules(lines)
    unique_molecules = find_single_replaces(rules, molecule)
    print(f'Distinct molecules after one step: {len(unique_molecules)}')
    steps = steps_to_create_molecule(rules, molecule)
    print(f'Steps needed to create molecule: {steps}')


def steps_to_create_molecule(rules, molecule):
    """Find number of steps needed to create molecule, using rules."""
    replaces_to_rule = sorted(get_replaces_to_rule(rules),
                              key=lambda item: len(item[0]),
                              reverse=True)
    start_molecule = molecule
    steps = 0
    while molecule != 'e':
        no_replaces = True
        steps += 1
        for replace, rule in replaces_to_rule:
            if replace in molecule:
                molecule = molecule.replace(replace, rule, 1)
                no_replaces = False
                break
        if no_replaces:
            # Reddit inspired shuffle
            random.shuffle(replaces_to_rule)
            molecule = start_molecule
            steps = 0
    return steps


def get_replaces_to_rule(rules):
    """Invert rules dictionary to list of (replace, rule) tuples."""
    replaces = []
    for rule, rule_replaces in rules.items():
        for replace in rule_replaces:
            replaces.append((replace, rule))
    return replaces


def find_single_replaces(rules, molecule):
    """Find all single replaces of rules in molecule."""
    replaces = set()
    for rule, rule_replaces in rules.items():
        for replace in rule_replaces:
            replaces = replaces | find_replaces(rule, replace, molecule)
    return replaces


def find_replaces(rule, replace, molecule):
    """Find possible replaces of rule in molecule."""
    replaces = set()
    for index in find_string(rule, molecule):
        replaces.add(
            ''.join((molecule[0:index], replace, molecule[index + len(rule):]))
        )
    return replaces


def find_string(string, text):
    """Find string in text. As generator return indexes one-by-one."""
    index = 0
    while 0 <= index < len(text):
        next_index = text.find(string, index)
        if next_index == -1:
            break
        yield next_index
        index = next_index + 1


def parse_rules(lines):
    """Parse rules from lines."""
    rules = defaultdict(list)
    for line in lines.split('\n'):
        rule, replace = parse_rule(line)
        rules[rule].append(replace)
    return rules


def parse_rule(line):
    """Parse line with rules to rule and replace tuple."""
    rule, replace = line.split(' => ')
    return rule, replace


def get_file_contents(file):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
