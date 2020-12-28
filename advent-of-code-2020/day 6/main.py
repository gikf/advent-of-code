# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:33:29 2020
"""


def main():
    groups = parse_groups(get_file_contents())
    group_any_answers = filter_group_answers(groups, filter_any_answer)
    print(f'Groups: {len(groups)}')
    any_question_answered = sum(len(group) for group in group_any_answers)
    print(f'Any question answered: {any_question_answered}')
    group_all_answers = filter_group_answers(groups, filter_all_answers)
    all_questions_answered = sum(len(group) for group in group_all_answers)
    print(f'All questions answered in groups: {all_questions_answered}')


def parse_groups(groups):
    """Parse groups separated by empty element."""
    parsed_groups = []
    cur_group = []
    for person in groups:
        if not person:
            parsed_groups.append(cur_group)
            cur_group = []
        else:
            cur_group.append(person)
    parsed_groups.append(cur_group)
    return parsed_groups


def filter_group_answers(groups, group_filter):
    """Filter answers from groups using group_filter."""
    return [group_filter(group) for group in groups]


def filter_any_answer(group):
    """Filter questions answered by anyone in group."""
    answers = set()
    for person in group:
        for question in person:
            answers.add(question)
    return answers


def filter_all_answers(group):
    """Filter questions answered by everybody in group."""
    answers = set(group[0])
    for person in group[1:]:
        answers = answers & set(person)
    return answers


def get_file_contents(file="input.txt"):
    """Read all lines from file."""
    with open(file) as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    main()
