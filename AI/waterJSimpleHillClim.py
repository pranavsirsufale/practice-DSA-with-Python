jar1Cap, jar2Cap = 4, 3
goal = (2, 0)
initialState = (0, 0)

def firstToSecond(x, y):
    transfer = min(x, jar2Cap-y)
    newx = x - transfer
    newy = y = transfer
    return (newx, newy)

def secondToFirst(x, y):
    transfer = min(y, jar1Cap-x)
    newx = x + transfer
    newy = y - transfer
    return (newx, newy)

def nextStates(x, y):
    return [
        (jar1Cap, y),
        (x, jar2Cap),
        (0, y),
        (x, 0),
        firstToSecond(x, y),
        secondToFirst(x, y)
    ]

def heuristic(state):
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

def simpleHillClimb():
    current = initialState
    visited = set()

    print("Steps: ")

    while current != goal:
        print(current)
        visited.add(current)

        neighbors = nextStates(current[0], current[1])
        nextState = None
        bestH = float('inf')

        for state in neighbors:
            if state not in visited:
                h = heuristic(state)
                if h < bestH:
                    bestH = h
                    nextState = state
        
        if nextState is None:
            print("Stuck! No better state found.")
            break

        current = nextState
    return current

solution = simpleHillClimb()

print("Goal State:", solution)

"""
Algorithm:
1. Evaluate the initial state. If it is also a goal state, then return it and quit. Otherwise,
continue with the initial state as the current state.
2. Loop until a solution is found or until there are no new operators left to be applied in the
current state:
    a) Select an operator that has not yet been applied to the current state and apply it to
    produce a new state.
    b) Evaluate the new state:
        i. If it is a goal state, then return it and quit.
        ii. If it is not a goal state but it is better than the current state, then make it the current
        state.
        iii. If it is not better than the current state, then continue in the loop.
"""
