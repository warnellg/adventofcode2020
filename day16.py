import re


# ==============================================================================
# HELPER FUNCTIONS
def parseTicket(lines):
    # index to keep track of where we are as we process input
    idx = 0

    # first set of entries is the fields and valid ranges
    fields = []
    rx = r'([\w\s]+): (\d+)-(\d+) or (\d+)-(\d+)'
    p = re.compile(rx)
    while lines[idx]:
        # extract what we need via regex
        m = p.match(lines[idx])
        name = m.group(1)

        # create function handle to check for validity
        is_valid = lambda x, lb1 = int(m.group(2)), ub1 = int(m.group(3)),\
                          lb2 = int(m.group(4)), ub2 = int(m.group(5)):\
                    ((x >= lb1) and (x <= ub1)) or ((x >= lb2) and (x <= ub2))

        # add to list of fields
        fields.append([name, is_valid])
        idx += 1

    # next entry is my ticket
    idx += 2
    myticket = [int(num) for num in lines[idx].split(',')]

    idx += 3
    nearbytickets = []
    while idx < len(lines):
        nearbytickets.append([int(num) for num in lines[idx].split(',')])
        idx += 1

    return fields, myticket, nearbytickets


# ==============================================================================
# PART 1
# read input and separate lines
with open('input/day16input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# parse input
fields, myticket, nearbytickets = parseTicket(lines)

# compute error rate
error_rate = 0
nearbytickets_valid = []
for ticket in nearbytickets:
    ticket_valid = True
    for val in ticket:
        # only add this value if its not valid for _any_ field
        if not any([field[1](val) for field in fields]):
            error_rate += val
            ticket_valid = False

    # build this here for part 2
    if ticket_valid:
        nearbytickets_valid.append(ticket)

answer_p1 = error_rate
print('Part 1:', answer_p1)


# ==============================================================================
# PART 2
# for each position, get the list of fields for which all values at this
# position are valid
validfields_at_pos = {}
for pos in range(len(fields)):
    validfields_at_pos[pos] = [field for field in fields if
                               all([field[1](ticket[pos]) for
                                    ticket in nearbytickets_valid])]

# use process of elimination to lock a single field at each position
field_positions = {}
while len(field_positions) != len(fields):
    # get subset of positions for which only one field is valid
    single_field_positions = [pos for pos in validfields_at_pos if
                              len(validfields_at_pos[pos]) == 1]

    for pos in single_field_positions:
        # get the corresponding field name
        field = validfields_at_pos[pos][0]

        # record the position
        field_positions[field[0]] = pos

        # remove this field from entries at other positions
        for pos2 in validfields_at_pos:
            if field in validfields_at_pos[pos2]:
                validfields_at_pos[pos2].remove(field)

# get answer by computing product of "departure" fields on _my_ ticket
product = 1
for field in fields:
    if 'departure' in field[0]:
        product *= myticket[field_positions[field[0]]]

answer_p2 = product
print('Part 2:', answer_p2)


print('Complete!')
