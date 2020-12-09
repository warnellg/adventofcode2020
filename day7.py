import re

# ======================================================================
# HELPER FUNCTIONS
def parseStatement(statement):
    # define some regexs for parsing
    rx_parent = r'(\w+ \w+) bags'
    p_parent = re.compile(rx_parent)
    rx_child = r'(\d+) (\w+ \w+) bags*'
    p_child = re.compile(rx_child)
    rx_split = r'[,.]\s*\n*'
    p_split = re.compile(rx_split)

    # split parent from children
    bagGroups = statement.split('contain ')

    # parse parent bag identifier
    m_parent = p_parent.match(bagGroups[0])
    parent = m_parent.group(1)

    # parse child bag identifier(s)
    childrenStatements = p_split.split(bagGroups[1])
    children = []
    for childStatement in childrenStatements[:-1]:
        m_child = p_child.match(childStatement)
        if m_child:
            children.append([int(m_child.group(1)), m_child.group(2)])

    return parent, children


def getBagsContained(graph, bag):
    # get children
    children = graph[bag]

    # start counting number of bags contained
    nContained = 0
    for child in children:
        # child entry is (#,type), so multiply # by (1+bags contained in type)
        # add the extra 1 because the bag itself counts, too
        nContained += child[0]*(1+getBagsContained(graph, child[1]))

    return nContained


# ======================================================================
# PART 1
# read input and separate lines
with open('input/day7input.txt', 'r') as f:
    text = f.read()
    statements = text.splitlines()

# build a directed graph using a dict where keys are bags and values are parents
bagGraph = {}
for statement in statements:
    # parse statement and add to graph
    parent, children = parseStatement(statement)
    for child in children:
        if child[1] in bagGraph.keys():
            bagGraph[child[1]].append(parent)
        else:
            bagGraph[child[1]] = [parent]

# search directed graph to find possible containers for 'shiny gold'
containers = [bagGraph['shiny gold']]
containers_added = []
containerCount = 0
while containers:
    # add these containers to the count (if not already there)
    for bag in containers[0]:
        # if not already added, increment count, add parents log
        if bag not in containers_added:
            containerCount += 1
            if bag in bagGraph.keys():
                containers.append(bagGraph[bag])
            containers_added.append(bag)

    # done with this level
    containers.pop(0)

print('Total number of containers is {}'.format(containerCount))


# ======================================================================
# PART 2
# build a directed graph using a dict where keys are bag type and values are [#, child bag type]
bagGraph2 = {}
for statement in statements:
    # parse statement and add to graph
    parent, children = parseStatement(statement)
    bagGraph2[parent] = children

# call recursive function to compute number of bags contained
bagsContained = getBagsContained(bagGraph2, 'shiny gold')


print('Total number of bags contained is {}.'.format(bagsContained))
