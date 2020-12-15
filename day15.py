# ======================================================================
# HELPER FUNCTIONS
def getLastNumber(preamble, turn_max):
    dictNum = {preamble[i]: [i + 1, -1] for i in range(len(preamble))}

    turn = len(preamble) + 1
    num_last = preamble[-1]
    while turn <= turn_max:
        if dictNum[num_last][1] == -1:
            # had been spoken before, but last time was the first time spoken
            num_last = 0
        else:
            # had been spoken before, but last time was not the first time
            num_last = dictNum[num_last][0] - dictNum[num_last][1]

        if num_last not in dictNum.keys():
            dictNum[num_last] = [turn, -1]
        else:
            dictNum[num_last][1] = dictNum[num_last][0]
            dictNum[num_last][0] = turn

        turn += 1

    return num_last


# ======================================================================
# PART 1
# puzzle input (part 1)
input = [11,18,0,20,1,7,16]
turn_max = 2020

num_last = getLastNumber(input, turn_max)

answer_p1 = num_last
print('Part 1:', answer_p1)


# ======================================================================
# PART 2
# puzzle input (part 2)
input = [11,18,0,20,1,7,16]
turn_max = 30000000

num_last = getLastNumber(input, turn_max)

answer_p2 = num_last
print('Part 2:', answer_p2)


print('Complete!')
