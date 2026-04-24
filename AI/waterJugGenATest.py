jar1Cap, jar2Cap = 4, 3
initialState = (0, 0)
goalState = (2, 0)

def pourFromFirstToSecond(x, y):
    transfer = min(x, jar2Cap-y)
    newX = x - transfer
    newY = y + transfer
    return (newX, newY)

def pourFromSecondToFirst(x, y):
    transfer = min(y, jar1Cap-x)
    newX = x + transfer
    newY = y - transfer
    return (newX, newY)

def generateAndtest():
    visitedStates = set()
    stack = [initialState]
    parentState = {}

    while stack:
        currentState = stack.pop()

        if currentState in visitedStates:
            continue

        visitedStates.add(currentState)
        if currentState == goalState:
            return reconstructPath(parentState, currentState)
        
        x, y = currentState

        nextStates = [
            (jar1Cap, y),
            (x, jar2Cap),
            (0, y),
            (x, 0),
            pourFromFirstToSecond(x, y),
            pourFromSecondToFirst(x, y)
        ]

        for nextState in nextStates:
            if nextState not in visitedStates:
                parentState[nextState] = currentState
                stack.append(nextState)
        
    return None

def reconstructPath(parentState, state):
    path = []
    while state:
        path.append(state)
        state = parentState.get(state)
    return path[::-1]

solution = generateAndtest()

if solution:
    print("solution path")
    for step in solution:
        print(step)