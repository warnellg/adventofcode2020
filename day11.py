import numpy as np


# ======================================================================
# HELPER FUNCTIONS
def linesToGrid(lines):
    # turn lines into a matrix
    # 0: floor (.)
    # 1: empty seat (L)
    # 2: occupied seat (#)
    n_rows = len(lines)
    n_cols = len(lines[0])
    occ_grid = np.zeros((n_rows, n_cols))
    for i in range(n_rows):
        for j in range(n_cols):
            if lines[i][j] == '.':
                occ_grid[i][j] = 0
            elif lines[i][j] == 'L':
                occ_grid[i][j] = 1
            else:
                occ_grid[i][j] = 2

    return occ_grid


def gridToLines(occ_grid):
    lines = []
    for i in range(np.shape(occ_grid)[0]):
        line = ''
        for j in range(np.shape(occ_grid)[1]):
            if occ_grid[i, j] == 0:
                line += '.'
            elif occ_grid[i, j] == 1:
                line += 'L'
            else:
                line += '#'
        lines.append(line)

    return lines


def evolveGrid(occ_grid):
    n_rows = np.shape(occ_grid)[0]
    n_cols = np.shape(occ_grid)[1]
    idx_grid = np.meshgrid(np.arange(n_cols), np.arange(n_rows))
    new_grid = occ_grid.copy()
    for i in range(n_rows):
        for j in range(n_cols):
            # get subarray with 8-connected neighbors
            nbhd = \
                occ_grid[np.logical_and(
                    np.logical_and((i-1) <= idx_grid[1], idx_grid[1] <= (i+1)),
                    np.logical_and((j-1) <= idx_grid[0], idx_grid[0] <= (j+1)))]

            # modify new grid based on rules
            if (occ_grid[i, j] == 1) and np.all(nbhd < 2):
                new_grid[i, j] = 2
            if (occ_grid[i, j] == 2) and (np.count_nonzero(nbhd == 2) > 4):
                # strictly greater than since this seat is in the nbhd
                new_grid[i, j] = 1

    return new_grid

def evolveGrid_visible(occ_grid):
    n_rows = np.shape(occ_grid)[0]
    n_cols = np.shape(occ_grid)[1]
    idx_grid = np.meshgrid(np.arange(n_cols), np.arange(n_rows))
    new_grid = occ_grid.copy()
    for i in range(n_rows):
        for j in range(n_cols):
            # get "visible" neighborhood
            nbhd = np.array([])
            i_b = i+1
            i_t = i-1
            j_l = j-1
            j_r = j+1
            idx_tl = [i_t, j_l]
            while (idx_tl[0] >= 0) and (idx_tl[1] >= 0):
                if occ_grid[idx_tl[0], idx_tl[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_tl[0], idx_tl[1]])
                    break
                idx_tl[0] -= 1
                idx_tl[1] -= 1
            idx_t = [i_t, j]
            while idx_t[0] >= 0:
                if occ_grid[idx_t[0], idx_t[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_t[0], idx_t[1]])
                    break
                idx_t[0] -= 1
            idx_tr = [i_t, j_r]
            while (idx_tr[0] >= 0) and (idx_tr[1] < n_cols):
                if occ_grid[idx_tr[0], idx_tr[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_tr[0], idx_tr[1]])
                    break
                idx_tr[0] -= 1
                idx_tr[1] += 1
            idx_r = [i, j_r]
            while idx_r[1] < n_cols:
                if occ_grid[idx_r[0], idx_r[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_r[0], idx_r[1]])
                    break
                idx_r[1] += 1
            idx_br = [i_b, j_r]
            while (idx_br[0] < n_rows) and (idx_br[1] < n_cols):
                if occ_grid[idx_br[0], idx_br[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_br[0], idx_br[1]])
                    break
                idx_br[0] += 1
                idx_br[1] += 1
            idx_b = [i_b, j]
            while idx_b[0] < n_rows:
                if occ_grid[idx_b[0], idx_b[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_b[0], idx_b[1]])
                    break
                idx_b[0] += 1
            idx_bl = [i_b, j_l]
            while (idx_bl[0] < n_rows) and (idx_bl[1] >= 0):
                if occ_grid[idx_bl[0], idx_bl[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_bl[0], idx_bl[1]])
                    break
                idx_bl[0] += 1
                idx_bl[1] -= 1
            idx_l = [i, j_l]
            while idx_l[1] >= 0:
                if occ_grid[idx_l[0], idx_l[1]] > 0:
                    nbhd = np.append(nbhd, occ_grid[idx_l[0], idx_l[1]])
                    break
                idx_l[1] -= 1
            # append at this index because thats what we did last time
            nbhd = np.append(nbhd, occ_grid[i, j])

            # modify new grid based on rules
            if (occ_grid[i, j] == 1) and np.all(nbhd < 2):
                new_grid[i, j] = 2
            if (occ_grid[i, j] == 2) and (np.count_nonzero(nbhd == 2) > 5):
                # strictly greater than since this seat is in the nbhd
                new_grid[i, j] = 1

    return new_grid


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day11input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# # build occupancy grid
# occ_grid = linesToGrid(lines)
#
# # evolve grid until stability
# occ_grid_old = np.array([])
# while not np.array_equal(occ_grid, occ_grid_old):
#     occ_grid_old = occ_grid
#     occ_grid = evolveGrid(occ_grid)
#
# # count number of occupied seats
# n_occupied = np.count_nonzero(occ_grid == 2)
# print('Number of occupied seats at stability:', n_occupied)


# ======================================================================
# PART 2
# build occupancy grid
occ_grid = linesToGrid(lines)

# evolve grid until stability
occ_grid_old = np.array([])
while not np.array_equal(occ_grid, occ_grid_old):
    occ_grid_old = occ_grid
    occ_grid = evolveGrid_visible(occ_grid)

# count number of occupied seats
n_occupied_visible = np.count_nonzero(occ_grid == 2)
print('Number of occupied seats at stability:', n_occupied_visible)


print('Complete!')
