import re


# ==============================================================================
# HELPER FUNCTIONS
def process_expression_simple(line):
    # simple evaluator (no parens)
    symbols = line.split(' ')
    value = int(symbols.pop(0))
    while symbols:
        # get operator
        op = symbols.pop(0)

        # apply operator to next value
        if op == '*':
            value = value * int(symbols.pop(0))
        else:
            value = value + int(symbols.pop(0))

    return value


def process_expression(line, part2=False):
    # list of operations that we'll evaluate in the right order at the very end
    # entries from left to right are values or operator strings
    expr_list = []

    # get lhs
    #   check for '(', recurse if found
    #   extract value
    #   check next character: if ')', remove it and return
    if line[0] == '(':
        # recurse on remainder of expression
        value_lhs, remainder = process_expression(line[1:], part2)
    else:
        # extract value
        value_lhs, remainder = extract_value(line)
    expr_list.append(value_lhs)

    # if next character is closed paren, remove it and return
    if line[0] == ')':
        value = evaluate_expression(expr_list, part2)
        return value, remainder[1:]

    # increment past the space and continue operator/value extraction
    remainder = remainder[1:]
    while remainder:
        # get operator
        op = remainder[0]
        remainder = remainder[2:]
        expr_list.append(op)

        # get rhs using same rules as lhs
        if remainder[0] == '(':
            # recurse on remainder of expression
            value_rhs, remainder = process_expression(remainder[1:], part2)
        else:
            # extract value
            value_rhs, remainder = extract_value(remainder)
        expr_list.append(value_rhs)

        # if string is empty or last character is closed paren, then return
        if not remainder or remainder[0] == ')':
            value = evaluate_expression(expr_list, part2)
            return value, remainder[1:]
        else:
            # otherwise, remove the space and continue
            remainder = remainder[1:]


def evaluate_expression(expr_list, part2=False):
    # lists will not have parens, so loop through once for all '+' since they
    # take precedence
    if part2:
        expr_list_sum = []
        idx = 0
        while idx < len(expr_list):
            if expr_list[idx] == '+':
                lhs = expr_list_sum.pop()
                product = lhs + expr_list[idx+1]
                expr_list_sum.append(product)
                idx += 2
            else:
                expr_list_sum.append(expr_list[idx])
                idx += 1
        expr_list = expr_list_sum

    # now only products to evaluate
    value = expr_list.pop(0)
    while expr_list:
        op = expr_list.pop(0)
        if op == '+':
            value = value + expr_list.pop(0)
        else:
            value = value * expr_list.pop(0)

    return value


def extract_value(line):
    p = re.compile(r'\d+')
    m = p.match(line)
    value_string = m.group()
    value = int(value_string)
    remainder = line[len(value_string):]

    return value, remainder


# ==============================================================================
# PART 1
# read input and separate lines
with open('input/day18input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# loop over each line
values = []
for line in lines:
    value, _ = process_expression(line)
    values.append(value)

sum_values = sum(values)

answer_p1 = sum_values
print('Part 1:', answer_p1)


# ==============================================================================
# PART 2
# loop over each line
values = []
for line in lines:
    value, _ = process_expression(line, part2=True)
    values.append(value)

sum_values = sum(values)

answer_p2 = sum_values
print('Part 2:', answer_p2)


print('Complete!')
