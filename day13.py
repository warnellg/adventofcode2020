import math

# ======================================================================
# HELPER FUNCTIONS
# find valid time for part 2 by searching over all t starting from 0
# nb: too slow!
def findValidTime(busConstraints):
    t = 0
    while True:
        # check t against all the constraints
        isValid = True
        for busConstraint in busConstraints:
            isValid_bus = (busConstraint[0] - (t % busConstraint[0])) % \
                          busConstraint[0] \
                          == busConstraint[1]
            if not isValid_bus:
                isValid = False
                break
        if isValid:
            break
        else:
            t += 1

    return t

# get lcm
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# find valid time for part 2 by successively building the desired pattern
def findValidTimeFast(busConstraints):
    # initialize time index to search over and increment
    t = 1
    t_inc = 1

    # loop over each constraint successively
    busConstraints.sort()
    for busConstraint in busConstraints:
        # add increment until we satisfy this constraint
        while (t % busConstraint[0]) != (-busConstraint[1] % busConstraint[0]):
            t += t_inc
        # this index is the new increment
        t_inc = lcm(t_inc, busConstraint[0])

    return t


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day13input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# quick parse
t_min = int(lines[0])
busIDs = [int(busID) for busID in lines[1].split(',') if busID.isnumeric()]

# just need the minimum value of t_min mod busID
waitTimes = [[busID - (t_min % busID), busID] for busID in busIDs]
minWait, minBusID = min(waitTimes)

answer_p1 = minBusID*minWait
print('Part 1:', answer_p1)


# ======================================================================
# PART 2
# re-parse second line
busConstraints = [[int(busID), offset] for
                  (offset, busID) in enumerate(lines[1].split(',')) if
                  busID.isnumeric()]

# start looping over values of t
t_valid = findValidTimeFast(busConstraints)

answer_p2 = t_valid
print('Part 2:', answer_p2)


print('Complete!')
