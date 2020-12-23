import regex as re


# ==============================================================================
# HELPER FUNCTIONS
def extract_rules(lines):
    # go line by line
    rules = {}
    for line in lines:
        # get the rule index
        linesplit = line.split(':')
        idx_rule = int(linesplit[0])

        # process the remainder of the rule
        if '"' in linesplit[1]:
            # simple rules
            p = re.compile('"(\D)"')
            rules[idx_rule] = p.findall(linesplit[1])[0]
        else:
            # compositional rules
            p = re.compile('(\d+)\s*')
            rules[idx_rule] = []
            if '|' in linesplit[1]:
                # for an "or" rule, create a list of rules
                sublinesplit = linesplit[1].split('|')
                rules[idx_rule].append([int(num) for num in p.findall(sublinesplit[0])])
                rules[idx_rule].append([int(num) for num in p.findall(sublinesplit[1])])
            else:
                rules[idx_rule].append([int(num) for num in p.findall(linesplit[1])])

    return rules


def construct_regex(rule, rules, part2=False):
    if isinstance(rule, str):
        # if the rule itself is just a string, then return the string
        regex = rule
    elif len(rule) == 1:
        # if the rule is a list of rules to follow, build the matching string by
        # concatenating the regexes that result from traversing those rules
        regex = ''
        for idx_rule in rule[0]:
            if part2 and idx_rule == 8:
                # special case for rule 8 in part2
                regex_42 = construct_regex(rules[42], rules, part2)
                regex += '(?:' + regex_42 + ')+'
            elif part2 and idx_rule == 11:
                # special case for rule 11 in part2
                regex_42 = construct_regex(rules[42], rules, part2)
                regex_31 = construct_regex(rules[31], rules, part2)
                regex += '((?:' + regex_42 + ')(?1)?(?:' + regex_31 + '))'
            else:
                regex += construct_regex(rules[idx_rule], rules, part2)
    else:
        # this is an "or" rule, so we need to use regex formatting to construct
        # it
        lhs = ''
        for idx_rule in rule[0]:
            lhs += construct_regex(rules[idx_rule], rules, part2)
        rhs = ''
        for idx_rule in rule[1]:
            rhs += construct_regex(rules[idx_rule], rules, part2)
        regex = '(?:' + lhs + '|' + rhs + ')'

    return regex


# ==============================================================================
# PART 1
# read input and separate lines
with open('input/day19input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# extract rules from messages
lines_rules = []
for i, line in enumerate(lines):
    if line:
        lines_rules.append(line)
    else:
        break
lines_messages = lines[i+1:]

# process rule lines to get a format we can work with
rules = extract_rules(lines_rules)

# construct the regex for the specified rule (0)
rx = construct_regex(rules[0], rules)
p = re.compile(rx)

# check messages for matches
n_matches = 0
for line in lines_messages:
    m = p.fullmatch(line)
    if m:
        n_matches += 1

answer_p1 = n_matches
print('Part 1:', answer_p1)


# ==============================================================================
# PART 2
# construct the regex for the specified rule taking into account the modified
# rules
rx = construct_regex(rules[0], rules, part2=True)
p = re.compile(rx)

# check messages for matches
n_matches = 0
for line in lines_messages:
    m = p.fullmatch(line)
    if m:
        n_matches += 1

answer_p2 = n_matches
print('Part 2:', answer_p2)


print('Complete!')
