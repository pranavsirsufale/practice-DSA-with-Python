from queue import PriorityQueue
jar1Cap, jar2Cap = 4, 3
initial = (0, 0)
goal = (2, 0)
OPEN = PriorityQueue()
CLOSED = set()
OLD = set()
parent = {}
cost = {}

def heuristic(state):
    return abs(state[0]-goal[0]) + abs(state[1]-goal[1])

def firstToSecond(x, y):
    transfer = min(x, jar2Cap-y)
    newx = x - transfer
    newy = y + transfer
    return newx, newy

def secondToFirst(x, y):
    transfer = min(y, jar1Cap-x)
    newx = x + transfer
    newy = y - transfer
    return (newx, newy)

def successors(x, y):
    return [
        (jar1Cap, y),
        (x, jar2Cap),
        (0, y),
        (x, 0),
        firstToSecond(x, y),
        secondToFirst(x, y)
    ]

def bestFirstSearch():
    OPEN.put((heuristic(initial), initial))
    OLD.add(initial)
    parent[initial] = None
    cost[initial] = 0

    while not OPEN.empty():
        _, current = OPEN.get()
        CLOSED.add(current)
        if current == goal:
            break

        for s in successors(current[0], current[1]):
            newCost = cost[current] + 1

            if s not in OLD:
                OLD.add(s)
                parent[s] = current
                cost[s] = newCost
                OPEN.put((heuristic(s), s))

            elif newCost < cost.get(s, float('inf')):
                parent[s] = current
                cost[s] = newCost
                OPEN.put((heuristic(s), s))
        
    path = []
    node = goal
    while node:
        path.append(node)
        node = parent[node]

    path.reverse()
    print("Steps")
    for p in path:
        print(p)
    
    print("goal State", goal)

bestFirstSearch()


"""
Algorithm:
1. Start with OPEN containing just the initial state.
2. Until a goal is found or there are no nodes left on OPEN do:
    a) Pick the best node on OPEN.
    b) Generate its successors.
    c) For each successor do:
        i. If it has not been generated before, evaluate it, add it to OPEN, and record its parent.
        ii. If it has been generated before, change the parent if this new path is better than the
        previous one. In that case, update the cost of getting to this node and to any successors
        that this node may already have.
"""