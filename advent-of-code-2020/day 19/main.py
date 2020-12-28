# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 19:06:18 2020
"""
import re


def main():
    input_data = get_file_contents().strip().split('\n\n')
    rules, messages = parse_input(input_data)

    matches = matching_messages(messages, rules, 0)
    print(len(matches))
    print(len(match_for_part2(rules, messages, 0)))


def match_for_part2(rules, messages, rule_number):
    """Filter messages matching rule_number, with modified rules for part 2."""
    counter1, counter2 = 0, -1
    pass_number = 2
    while counter1 != counter2:
        rule_modify = ' |' if pass_number > 2 else ''
        rules[8] = f'42{rule_modify}' + ' |'.join(
            ' 42' * n for n in range(2, pass_number)
        )
        rules[11] = f'42 31{rule_modify}' + ' |'.join(
            ' 42' * n + ' 31' * n for n in range(2, pass_number)
        )
        expression = rule_regex(rule_number, rules)
        matching = []
        for message in messages:
            if re.match(f'^{expression}$', message):
                matching.append(message)
        counter2, counter1 = counter1, len(matching)
        pass_number += 1
    return matching


def parse_rules(input_rules):
    """Parse rules from input_rules."""
    rules = {}
    for rule in input_rules.split('\n'):
        number, requirements = rule.split(': ')
        rules[int(number)] = requirements.strip('"')
    return rules


def rule_regex(rule_number, rules):
    """Create rule_number regex from rules."""
    if rules[rule_number] in 'ab':
        return rules[rule_number]
    sub_rules = rules[rule_number].split(' | ')
    for index, sub_rule in enumerate(sub_rules):
        sub_rule_regex = ''.join(rule_regex(int(number), rules)
                                 for number in sub_rule.split())
        sub_rules[index] = f'({sub_rule_regex})'
    return '(' + '|'.join(sub_rules) + ')'


def matching_messages(messages, rules, rule_number):
    """Filter messages matching rule_number from rules"""
    return [
        message
        for message in messages
        if bool(re.match(f'^{rule_regex(rule_number, rules)}$', message))
    ]


def parse_input(input_data):
    """Parse input data to rules and messages."""
    rules, messages = input_data
    return parse_rules(rules), parse_messages(messages)


def parse_messages(messages):
    """Parse messages."""
    return [message.strip() for message in messages.split('\n')]


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.read()


if __name__ == '__main__':
    main()
