jar1Cap, jar2Cap = 4, 3
goal = (2, 0)
initial = (0, 0)

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

def waterJugSteepestHillClimbing():
    current = initial
    visited = set()
    print("STEPS: ")

    while current != goal:
        print(current)
        visited.add(current)

        neighbours = nextStates(current[0], current[1])
        unvisited = [s for s in neighbours if s not in visited]

        if not unvisited:
            print("No more move possible!")
            break

        current = min(unvisited, key=heuristic)
    
    return current

solution = waterJugSteepestHillClimbing()

print("goal State", solution)


"""
Algorithm:
1. Evaluate the initial state. If it is also a goal state, then return it and quit. Otherwise,
continue with the initial state as the current state.
2. Loop until a solution is found or until a complete iteration produces no change to current
state:
    a) Let SUCC be a state such that any possible successor of the current state will be better
    than SUCC.
    b) For each operator that applies to the current state do:
        i. Apply the operator and generate a new state.
        ii. Evaluate the new state. If it is a goal state, then return it and quit. If not, compare it to
        SUCC. If it is better, then set SUCC to this state. If it is not better, leave SUCC alone.
        iii. If the SUCC is better than current state, then set current state to SUCC.
"""