import re
from collections import OrderedDict


# ======================================================================
# HELPER FUNCTIONS
NUM_BITS = 36

# function to parse input
def parseProgram(program):
    # define some regular expressions
    rx_mask = r'mask = (\w+)'
    p_mask = re.compile(rx_mask)
    rx_mem = r'mem\[(\d+)\] = (\d+)'
    p_mem = re.compile(rx_mem)

    # initialize return dict
    # use an ordered dictionary because later we'll want to process in reverse
    memOps = OrderedDict()

    # parse
    for instruction in program:
        m_mask = p_mask.match(instruction)
        if m_mask:
            # parse mask and create dictionary entry if one doesn't yet exist
            mask = m_mask.group(1)
            if mask not in memOps.keys():
                memOps[mask] = []
        else:
            m_mem = p_mem.match(instruction)
            memOps[mask].append([int(m_mem.group(1)), int(m_mem.group(2))])

    return memOps


# build a series of bits from a string (part 1)
def buildBitMasks(mask_string):
    # zerosmask: 0 where 0s, 1 where 1s or Xs
    # onesmask: 1 where 1s, 0 where 0s or Xs
    zerosmask = int(mask_string.replace('X', '1'), 2)
    onesmask = int(mask_string.replace('X', '0'), 2)

    return zerosmask, onesmask


# function to perform requested binary masking of each number (part 1)
def maskNum(num, zerosmask, onesmask):
    # apply zeros mask first
    num_zerosmask = num & zerosmask
    num_masked = num_zerosmask | onesmask

    return num_masked


# function to write to all the locations induced by (op, floatBits) pair
# (part 2)
def writeToFloatingAddresses(op, floatingBits, memDict):
    # get the modified address with/without the floating bit turned on
    op_floatbiton = [op[0] | (1 << floatingBits[0]), op[1]]
    op_floatbitoff = [op[0] & ~(1 << floatingBits[0]), op[1]]
    if len(floatingBits) == 1:
        # if there are no more floating bits to handle, perform the write
        memDict[op_floatbiton[0]] = op_floatbiton[1]
        memDict[op_floatbitoff[0]] = op_floatbitoff[1]
    else:
        # if there are more floating bits to handle, turn this one on/off and
        # recurse
        writeToFloatingAddresses(op_floatbiton, floatingBits[1:], memDict)
        writeToFloatingAddresses(op_floatbitoff, floatingBits[1:], memDict)


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day14input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# parse program
memOps = parseProgram(lines)

# run program chunks mask by mask
memDict = {}
for mask_string in memOps:
    zerosmask, onesmask = buildBitMasks(mask_string)
    for writeInstruction in memOps[mask_string]:
        memDict[writeInstruction[0]] = maskNum(writeInstruction[1],
                                               zerosmask, onesmask)

memSum = 0
for key in memDict.keys():
    memSum += memDict[key]

answer_p1 = memSum
print('Part 1:', answer_p1)


# ======================================================================
# PART 2
# process instructions backwards and keep special bitmask for what's already
# been processed
memDict2 = {}
for mask_string in memOps:
    # generate ones mask and find floating bits
    onesmask = int(mask_string.replace('X', '0'), 2)
    floatingBits = [(NUM_BITS-1-i) for i, char in enumerate(mask_string) if char == 'X']

    for memOp in memOps[mask_string]:
        # apply ones mask
        newOp = [memOp[0] | onesmask, memOp[1]]

        # perform the necessary writes
        writeToFloatingAddresses(newOp, floatingBits, memDict2)

memSum = 0
for key in memDict2.keys():
    memSum += memDict2[key]

answer_p2 = memSum
print('Part 2:', answer_p2)


print('Complete!')
