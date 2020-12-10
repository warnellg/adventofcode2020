import numpy as np


# ======================================================================
# HELPER FUNCTIONS
def countPaths(graph, start, end):
    # initialize number of paths to 0
    n_paths = 0

    if start == end:
        # if we reached the destination, then we have completed exactly 1 path
        n_paths = 1
    else:
        # if not at destination, then sum the number of paths that go to
        # destination starting at neighbors
        for node in graph[start]:
            n_paths += countPaths(graph, node, end)

    return n_paths


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day10input.txt', 'r') as f:
    text = f.read()
    lines = text.splitlines()

# build a list of the input joltage ratings, starting from 0
rating_init = 0
ratings = []
for line in lines:
    ratings.append(int(line))
rating_max = max(ratings)+3
ratings = np.array([rating_init] + ratings + [rating_max])
ratings_sorted = np.sort(ratings)

# use numpy to sort, compute diffs, and use rule on diffs to compute solution
ratings_diff = np.diff(ratings_sorted)
answer = np.count_nonzero(ratings_diff == 1) * \
         np.count_nonzero(ratings_diff == 3)

print('Number of 1-jolt difference times number of 3-jolt differences:', answer)


# ======================================================================
# PART 2
# build a graph over the ratings, including the init and max rating
# edges point FROM an adapter TO an adapter it could connect to (rating 3 or
# fewer jolts higher)
G_ratings = {}
for rating in ratings:
    G_ratings[rating] = ratings[ (ratings <= (rating+3)) & (ratings > rating)]

# search the graph for paths that start at rating_max and end at rating_min
# # generic path search is way too slow!
# n_paths = countPaths(G_ratings, rating_init, rating_max)

# use unique structure of graph to try to do things more efficiently
# in particular, look for "isolated" subgraphs where we can count the number of
# paths within and at the end multiply together the number of paths per subgraph
subgraph_npaths = []
subgraph_start = ratings_sorted[0]
for idx, rating in enumerate(ratings_sorted):
    if (rating == rating_max) or ((ratings_sorted[idx+1] - rating) == 3):
        # we've found the "last" node of a "subgraph"
        subgraph_end = rating
        n = countPaths(G_ratings, subgraph_start, subgraph_end)
        subgraph_npaths.append(n)

        # if we're not at the destination, set subgraph start to be next node
        if rating != rating_max:
            subgraph_start = ratings_sorted[idx+1]

# now compute answer by multiplying together all of the subgraph_npaths
n_paths = np.prod(np.array(subgraph_npaths))
print('Total number of adapter paths from start to finish:', n_paths)


print('Complete!')
