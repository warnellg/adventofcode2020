import re
import numpy as np


# ======================================================================
# HELPER FUNCTIONS
# direction-parsing function
def parseDirection(direction):
    # define regex and match
    rx = r'([NSEWLRF])(\d+)'
    p = re.compile(rx)
    m = p.match(direction)

    # pull out command and argument
    action = m.group(1)
    value = int(m.group(2))

    return action, value


# apply rotation
def rotate(coord, angle):
    # create rotation matrix
    R = np.array([[np.cos(angle), -np.sin(angle)],
                 [np.sin(angle), np.cos(angle)]])
    Rcoord = R.dot(coord)

    return Rcoord


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day12input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# start processing directions
# initialize state to be position at origin and facing east
# "facing east" is 0 degrees, "facing north" is +90 degrees
position = np.array([0., 0.])
facing = 0
for line in lines:
    action, value = parseDirection(line)

    if action == 'N':
        # north means increment second coordinate by value
        position[1] += value
    elif action == 'S':
        # south means decrement second coordinate by value
        position[1] -= value
    elif action == 'E':
        # east means increment first coordinate by value
        position[0] += value
    elif action == 'W':
        # west means decrement first coordinate by value
        position[0] -= value
    elif action == 'L':
        # turn left means increment facing direction by value
        facing = (facing + (value * np.pi / 180.)) % (2 * np.pi)
    elif action == 'R':
        # turn right means decrement facing direction by value
        facing = (facing - (value * np.pi / 180.)) % (2 * np.pi)
    elif action == 'F':
        # move forward
        position += value*np.array([np.cos(facing), np.sin(facing)])

answer_p1 = np.linalg.norm(position, 1)
print('Part 1:', answer_p1)


# ======================================================================
# PART 2
# re-process directions
position_waypoint = np.array([10., 1.])
position_ship = np.array([0., 0.])
for line in lines:
    action, value = parseDirection(line)

    if action == 'N':
        # north means move waypoint north relative to ship
        position_waypoint[1] += value
    elif action == 'S':
        # south means move waypoint south relative to ship
        position_waypoint[1] -= value
    elif action == 'E':
        # east means move waypoint east relative to ship
        position_waypoint[0] += value
    elif action == 'W':
        # west means move waypoint west relative to ship
        position_waypoint[0] -= value
    elif action == 'L':
        # L means to rotate waypoint around the ship counterclockwise
        position_waypoint = rotate(position_waypoint, (value * np.pi / 180.))
    elif action == 'R':
        # R means to rotate waypoint around the ship clockwise
        position_waypoint = rotate(position_waypoint, -(value * np.pi / 180.))
    elif action == 'F':
        # ship moves to waypoint
        position_ship += value*position_waypoint

answer_p2 = np.linalg.norm(position_ship, 1)
print('Part 2:', answer_p2)


print('Complete!')
