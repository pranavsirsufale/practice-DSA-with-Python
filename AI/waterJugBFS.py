from collections import deque
X, Y = 4, 3
initialState = (0, 0)
goalState = (2, 0)

def BFS():
    nodeList = deque([initialState])
    visitedStates = set()
    parentState = {}

    while nodeList:
        currentState = nodeList.popleft()
        if currentState in visitedStates:
            continue
        visitedStates.add(currentState)
        if currentState == goalState:
            return reconstructPath(parentState, currentState)
        
        x, y = currentState
        nextStates = [(X, y), (x, Y), (0, y), (x, 0),
                    (max(0, x-(Y-y)), min(Y, y+x)),
                    (min(X, x+y), max(0, y - (X-x)))
                    ]
        
        for nextState in nextStates:
            if nextState not in visitedStates:
                parentState[nextState] = currentState
                nodeList.append(nextState)
    return None

def reconstructPath(parentState, state):
    path = []
    while state:
        path.append(state)
        state = parentState.get(state)
    return path[::-1]

solution = BFS()
if solution:
    for step in solution:
        print(step)
    else:
        print("No solution found")

"""
Algorithm:
1. Create a variable called NODE-LIST and set it to the initial state.
2. Until a goal state is found or nodeList is empty:
    a) Remove the first element from nodeList and call it 'currentState', if nodeList was empty quit.
    b) for each way that each rule can match the state described in 'currentState' do:
        i. apply the rule to generate a new state.
        ii. if the new state is the goal state, quit and return this state.
        iii. otherwise, add the new state to the end of the nodeList.
"""