# ======================================================================
# HELPER FUNCTIONS
# function to check validity of a given number in the context of a window
# number is valid if it is the sum of two different numbers in the window
def checkValidity(num, window):
    isValid = False
    while window:
        # subtract first element of window from num
        diff = num - window[0]
        # remove first element from window and search for diff
        window.pop(0)
        if diff in window:
            isValid = True
            break

    return isValid


# ======================================================================
# PART 1
# explicitly hard-coded quantities
LENGTH_PREAMBLE = 25

# read input and separate lines
with open('input/day9input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# turn numbers on each line into a list
numbers = []
for line in lines:
    numbers.append(int(line))

# initialize sliding window of numbers with the preamble and loop over subsequent numbers
window = numbers[0:LENGTH_PREAMBLE]
for num in numbers[LENGTH_PREAMBLE:]:
    # check number for validity in the context of current
    # when passing list `window` to function, pass a deep copy
    isValid = checkValidity(num, window.copy())
    if isValid:
        # if valid, update sliding window and proceed
        window.pop(0)
        window.append(num)
    else:
        # if invalid, report and break
        invalidNum = num
        print('Number {} failed validity check.'.format(invalidNum))
        break


# ======================================================================
# PART 2

for startIdx in range(len(numbers)):
    # start looping over number list from this starting point
    minNum = numbers[startIdx]
    maxNum = numbers[startIdx]
    runningSum = 0
    for endIdx in range(startIdx, len(numbers)):
        # add current number to running sum
        runningSum += numbers[endIdx]

        # update min and max if necessary
        if numbers[endIdx] < minNum:
            minNum = numbers[endIdx]
        if numbers[endIdx] > maxNum:
            maxNum = numbers[endIdx]

        # check to see if sum is equal to invalid number
        if runningSum == invalidNum:
            # compute sum of first and last number in the running sum
            answerSum = minNum + maxNum
            print('Found solution. Sum of min and max is {}.'.format(answerSum))
            break
        if runningSum > invalidNum:
            # can't get smaller so move on
            break

    # break this loop too if we found the correct answer
    if runningSum == invalidNum:
        break

print('Complete!')
