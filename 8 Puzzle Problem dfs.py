GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move_tile(state, x1, y1, x2, y2):
    new_state = [row[:] for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def dfs(start):
    stack = [(start, [])]  # Stack to hold states and their paths
    visited = set() 

    while stack:
        current, path = stack.pop()
        visited.add(tuple(map(tuple, current)))

        if current == GOAL_STATE:
            return path

        x, y = find_blank(current)
        moves = []
        if x > 0: moves.append(move_tile(current, x, y, x-1, y)) 
        if x < 2: moves.append(move_tile(current, x, y, x+1, y))  
        if y > 0: moves.append(move_tile(current, x, y, x, y-1))  
        if y < 2: moves.append(move_tile(current, x, y, x, y+1))  

        for move in moves:
            if tuple(map(tuple, move)) not in visited:
                stack.append((move, path + [move]))

    return None

def get_input():
    print("Enter your 8-puzzle state (0 for blank):")
    state = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        state.append(row)
    return state

initial_state = get_input()
solution = dfs(initial_state)

if solution:
    print("Puzzle solved using DFS!")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No solution found.")
