#!/usr/bin/python3

import sys


def cartesian_product(left, right):
    if isinstance(left, str):
        if isinstance(right, str):
            return [left + right]
        return [left + string for string in right]

    if isinstance(right, str):
        return [string + right for string in left]

    result = []
    for left_string in left:
        for right_string in right:
            result.append(left_string + right_string)
    return result

def parse(expr, delimiter=' '):
    '''
    Given an expression, compute the result of `echo`ing it.

    This procedure uses a stack and scans the expression, resulting in one of
    these cases:
        {: Push onto stack. It is needed for the complementing opening brace.
        ,: Check top of stack for opening brace or comma. This is for edge
            cases where a comma comes right after an opening brace or another
            comma, so push an empty string. Push comma onto stack regardless
            because it is the delimiter for elements in braces.
        }: Pop the stack to form a group until an opening brace is found,
            completing the group. Construct a new group from the Cartesian
            product of that group and the element preceding the opening brace,
            then push the new group onto the stack. Edge cases are handled
            here, e.g. braces that are not well-formed or a closing brace
            comes right after a comma.
        default: Check the top of the stack, using the result to determine if
            it should be pushed back, concatenated, or used for Cartesian
            product.

    After scanning the string, the stack should contain only strings or lists
    of strings. All remaining Cartesian products are computed.
    '''

    stack = []

    def pop_or_default(default=''):
        try:
            return stack.pop()
        except IndexError:
            return default

    for char in expr:
        if char == '{':
            stack.append(char)
        elif char == ',':
            last_element = pop_or_default()
            if last_element != ',':
                stack.append(last_element)
            if last_element == '{' or last_element == ',':
                stack.append('')

            stack.append(char)
        elif char == '}':
            group = []

            while stack and stack[-1] != '{':
                group.insert(0, stack.pop())

            opening_brace, last_element = pop_or_default(), pop_or_default()

            if not group:
                group = ['']
            if len(group) == 1 and opening_brace:
                group = cartesian_product('{', group)
                group = cartesian_product(group, '}')
            if len(group) == 1 and not opening_brace:
                group = cartesian_product(group[0], '}')
            if group[-1] == ',':
                group[-1] = ''

            new_group = []
            if isinstance(last_element, str):
                for element in group:
                    new_group.extend(cartesian_product(last_element, element))
            else:
                new_group.extend(cartesian_product(last_element, group))

            stack.append(new_group)
        else:
            last_element = pop_or_default()

            if last_element == ',':
                stack.append(char)
            elif isinstance(last_element, str) and last_element != '{':
                stack.append(last_element + char)
            elif isinstance(last_element, list):
                stack.append(cartesian_product(last_element, char))
            else:
                stack.append(last_element)
                stack.append(char)

    flattened_list = ['']
    while stack:
        last_element = stack.pop()
        flattened_list = cartesian_product(last_element, flattened_list)

    return delimiter.join(flattened_list)

if __name__ == '__main__':
    expr = sys.argv[1]
    result = parse(expr)
    print(result)
