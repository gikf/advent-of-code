# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 17:59:31 2020
"""
import re


OPERATORS = '+*'
OPERATIONS = {
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
}


def main():
    lines = [line.strip() for line in get_file_contents()]
    expressions_with_same_operator_order = parse_expressions(lines, {
        '+': 2,
        '*': 2,
    })
    expressions_with_addition_higher_order = parse_expressions(lines, {
        '+': 5,
        '*': 2,
    })
    evaluated_same_order = evaluate_expressions(
        expressions_with_same_operator_order)
    evaluated_addition_higher = evaluate_expressions(
        expressions_with_addition_higher_order)
    print('Sum of expressions with operators having the same precedence: '
          f'{sum(evaluated_same_order)}')
    print('Sum of expressions with addition having higher precedence: '
          f'{sum(evaluated_addition_higher)}')


def parse_expressions(lines, operator_order):
    """Parse expressions from lines."""
    parsed_expressions = []
    for line in lines:
        parsed_expressions.append(parse_expression(line, operator_order))
    return parsed_expressions


def parse_expression(line, operator_order):
    """Parse expression to postfix notation order with operator_order."""
    expression = re.sub(r'([\(\)])', r' \1 ', line).split()
    parsed_expression = []
    stack = []
    for element in expression:
        if element.isdigit():
            parsed_expression.append(int(element))
        elif element in OPERATORS:
            if not stack or stack[-1] == '(':
                stack.append(element)
            elif operator_order[element] > operator_order[stack[-1]]:
                stack.append(element)
            else:
                while (
                    stack
                    and stack[-1] != '('
                    and operator_order[element] <= operator_order[stack[-1]]
                ):
                    parsed_expression.append(stack.pop())
                stack.append(element)
        elif element == '(':
            stack.append(element)
        elif element == ')':
            while stack[-1] != '(':
                parsed_expression.append(stack.pop())
            stack.pop()
    while stack:
        parsed_expression.append(stack.pop())
    return parsed_expression


def evaluate_expressions(expressions):
    """Evaluate expressions."""
    return [
        evaluate_expression(expression)
        for expression in expressions
    ]


def evaluate_expression(expression):
    """Evaluate expression in postfix notation."""
    stack = []
    for element in expression:
        if isinstance(element, int):
            stack.append(element)
        elif element in OPERATORS:
            num_b = stack.pop()
            num_a = stack.pop()
            stack.append(OPERATIONS[element](num_a, num_b))
    return stack[0]


def get_file_contents(file='input.txt'):
    """Read all lines from file."""
    with open(file) as f:
        return f.readlines()


if __name__ == '__main__':
    main()
