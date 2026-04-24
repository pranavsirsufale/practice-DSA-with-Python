from collections import deque
jar1Capacity, jar2Capacity = 4, 3
intialState = (0, 0)
goalstate = (2, 0)

def pourFirstToSecond(x, y):
    transfer = min(x, jar2Capacity - y)
    newX = x - transfer
    newY = y + transfer
    return (newX, newY)

def pourSecondToFirst(x, y):
    transfer = min(y, jar1Capacity - x)
    newX = x + transfer
    newY = y - transfer
    return (newX, newY)

def DFS():
    nodeList = deque([intialState])
    visitedStates = set()
    parentState = {}

    while nodeList:
        currentState = nodeList.popleft()
        print("PARENT STATE", parentState)
        if currentState in visitedStates:
            continue
        visitedStates.add(currentState)
        if currentState == goalstate:
            return reconstructPath(parentState, currentState)
        x, y = currentState
        nextStates = [
            (jar1Capacity, y),
            (x, jar2Capacity),
            (0, y),
            (x, 0),
            pourFirstToSecond(x, y),
            pourSecondToFirst(x, y)
        ]

        for nextState in nextStates:
            if nextState not in visitedStates:
                parentState[nextState] = currentState
                print(parentState)
                nodeList.appendleft(nextState)

    return None

def reconstructPath(parentState, state):
    path = []
    while state:
        path.append(state)
        state = parentState.get(state)
    return path[::-1]

solution = DFS()

foundSol = False
if solution:
    for step in solution:
        print(step)
        if step == goalstate:
            foundSol = True
    if foundSol:
        print("Solution is found")
    else:
        print("No solution found.")



"""
1. Initialize NODE-LIST with the initial state (0, 0).
2. Create an empty set for visited states.
3. Repeat until NODE-LIST is empty:
    a) Remove the first element from NODE-LIST → call it E.
    b) If E is the goal state, return the solution.
    c) If E is not visited:
        i. Mark E as visited.
        ii. Generate all possible next states.
        iii. Add new states to the FRONT of NODE-LIST.
"""