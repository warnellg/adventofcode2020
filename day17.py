import numpy as np


# ==============================================================================
# HELPER FUNCTIONS
def read_initial_state(lines):
    state = np.zeros((len(lines), len(lines[0])))
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                state[i, j] = 0
            else:
                state[i, j] = 1

    return state


def expand_state_3d(state, n_cycles):
    # first, consider in-plane radius of influence
    expanded_plane = np.zeros((state.shape[0] + 2*(n_cycles + 1),
                               state.shape[1] + 2*(n_cycles + 1)))
    expanded_plane[(n_cycles + 1):(n_cycles + 1 + state.shape[0]),
                   (n_cycles + 1):(n_cycles + 1 + state.shape[1])] = state

    # now pad above and below
    expanded_state = np.zeros((expanded_plane.shape[0], expanded_plane.shape[1],
                               1 + 2*(n_cycles + 1)))
    expanded_state[:, :, (n_cycles + 1)] = expanded_plane

    return expanded_state


def apply_cycle_3d(state):
    # loop over all cells with neighbors
    cycled_state = np.copy(state)
    range_nbhd_coord = (-1, 1)
    for x in range(1, state.shape[0] - 1):
        nbhd_x = slice(x + range_nbhd_coord[0], x + range_nbhd_coord[1] + 1)
        for y in range(1, state.shape[1] - 1):
            nbhd_y = slice(y + range_nbhd_coord[0], y + range_nbhd_coord[1] + 1)
            for z in range(1, state.shape[2] - 1):
                nbhd_z = slice(z + range_nbhd_coord[0], z + range_nbhd_coord[1] + 1)
                nbhd_mask = False * state[nbhd_x, nbhd_y, nbhd_z]
                nbhd_mask[1, 1, 1] = True
                nbhd = np.ma.masked_array(state[nbhd_x, nbhd_y, nbhd_z],
                                          mask=nbhd_mask)
                if state[x, y, z]:
                    if not ((np.sum(nbhd.flatten()) == 2) or
                            (np.sum(nbhd.flatten()) == 3)):
                        cycled_state[x, y, z] = 0.
                else:
                    if np.sum(nbhd.flatten()) == 3:
                        cycled_state[x, y, z] = 1.

    return cycled_state


def expand_state_4d(state, n_cycles):
    # first, consider in-plane radius of influence
    expanded_plane = np.zeros((state.shape[0] + 2*(n_cycles + 1),
                               state.shape[1] + 2*(n_cycles + 1)))
    expanded_plane[(n_cycles + 1):(n_cycles + 1 + state.shape[0]),
                   (n_cycles + 1):(n_cycles + 1 + state.shape[1])] = state

    # now pad above and below
    expanded_cube = np.zeros((expanded_plane.shape[0], expanded_plane.shape[1],
                              1 + 2*(n_cycles + 1)))
    expanded_cube[:, :, (n_cycles + 1)] = expanded_plane

    # now pad "above" and "below in 4th dimension
    expanded_state = np.zeros((expanded_cube.shape[0], expanded_cube.shape[1],
                               expanded_cube.shape[2], 1 + 2*(n_cycles + 1)))
    expanded_state[:, :, :, (n_cycles+1)] = expanded_cube

    return expanded_state


def apply_cycle_4d(state):
    # loop over all cells with neighbors
    cycled_state = np.copy(state)
    range_nbhd_coord = (-1, 1)
    for x in range(1, state.shape[0] - 1):
        nbhd_x = slice(x + range_nbhd_coord[0], x + range_nbhd_coord[1] + 1)
        for y in range(1, state.shape[1] - 1):
            nbhd_y = slice(y + range_nbhd_coord[0], y + range_nbhd_coord[1] + 1)
            for z in range(1, state.shape[2] - 1):
                nbhd_z = slice(z + range_nbhd_coord[0], z + range_nbhd_coord[1] + 1)
                for w in range(1, state.shape[3] - 1):
                    nbhd_w = slice(w + range_nbhd_coord[0], w + range_nbhd_coord[1] + 1)
                    nbhd_mask = False * state[nbhd_x, nbhd_y, nbhd_z, nbhd_w]
                    nbhd_mask[1, 1, 1, 1] = True
                    nbhd = np.ma.masked_array(state[nbhd_x, nbhd_y, nbhd_z, nbhd_w],
                                              mask=nbhd_mask)
                    if state[x, y, z, w]:
                        if not ((np.sum(nbhd.flatten()) == 2) or
                                (np.sum(nbhd.flatten()) == 3)):
                            cycled_state[x, y, z, w] = 0.
                    else:
                        if np.sum(nbhd.flatten()) == 3:
                            cycled_state[x, y, z, w] = 1.

    return cycled_state


# ==============================================================================
# PART 1
# read input and separate lines
N_CYCLES = 6
with open('input/day17input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# get initial state from input
state_init = read_initial_state(lines)

# expand state to maximum sphere of influence
state3d = expand_state_3d(state_init, N_CYCLES)

# perform six cycles
for i in range(N_CYCLES):
    state3d = apply_cycle_3d(state3d)

# compute total number of active cubes
n_active = np.sum(state3d.flatten())

answer_p1 = n_active
print('Part 1:', answer_p1)


# ==============================================================================
# PART 2
# apply same operations as above, just with the 4d versions
state4d = expand_state_4d(state_init, N_CYCLES)
for i in range(N_CYCLES):
    state4d = apply_cycle_4d(state4d)

# compute total number of active cubes
n_active = np.sum(state4d.flatten())

answer_p2 = n_active
print('Part 2:', answer_p2)


print('Complete!')
