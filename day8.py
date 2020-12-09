import re

# ======================================================================
# HELPER FUNCTIONS
# instruction-parsing function
def parseInstruction(instruction):
    # define regex and match
    rx = r'(\w+) ([\+\-])(\d+)'
    p = re.compile(rx)
    m = p.match(instruction)

    # pull out command and argument
    cmd = m.group(1)
    arg = int(m.group(3))
    if m.group(2) == '-':
        arg *= -1

    return cmd, arg


# instruction-creation function
def createInstruction(cmd, arg):
    instruction = cmd
    instruction += ' '
    if arg >= 0:
        instruction += '+' + str(arg)
    else:
        instruction += str(arg)

    return instruction


# loop-finding function (with accumulation)
def findLoop(instructions):
    # log for which instructions have already been executed
    visited = []

    # start processing instructions until we have a repeat
    acc = 0
    idx = 0
    while (idx not in visited) and (idx < len(instructions)):
        # add this line number to the list of visited
        visited.append(idx)

        # parse and process this instruction
        cmd, arg = parseInstruction(instructions[idx])
        if cmd == 'acc':
            # acc means add arg to accumulator and move forward one instruction
            acc += arg
            idx += 1
        elif cmd == 'jmp':
            # jump means move to instruction at relative position indicated by arg
            idx += arg
        elif cmd == 'nop':
            # nop means do nothing and move to next instruction
            idx += 1

    return idx, acc


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day8input.txt', 'r') as f:
    text = f.read()
    instructions = text.splitlines()

# find loop in program while accumulating
idx, acc = findLoop(instructions)
print('Accumulator value through first repeat: {}'.format(acc))


# ======================================================================
# PART 2
# loop over lines to possibly edit
for editIdx, instruction in enumerate(instructions):
    # parse this particular instruction to see if it is editable
    cmd, arg = parseInstruction(instruction)

    # edit instruction if allowed
    # edits allowed: [nop -> jmp] or [jmp -> nop]
    editedInstructions = instructions.copy()
    if cmd == 'jmp':
        # jmps change to nops
        editedInstruction = createInstruction('nop', arg)
        editedInstructions[editIdx] = editedInstruction
    elif cmd == 'nop':
        # nops change to jmps
        editedInstruction = createInstruction('jmp', arg)
        editedInstructions[editIdx] = editedInstruction
    else:
        continue

    # check edited instruction set for loop
    # if idx returned is off the end of the list of instructions, we've done it
    idx, acc = findLoop(editedInstructions)
    if idx == len(instructions):
        print('Loop removed by editing instruction [{}] at line {}. Final accumulator value is {}.'.format(instruction, editIdx, acc))
        break

print('Complete.')
