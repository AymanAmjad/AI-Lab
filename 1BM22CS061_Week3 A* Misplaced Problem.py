import heapq
GOAL_STATE = [[0, 1, 2], [3, 4, 5], [6, 7 ,8]]

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def move_tile(state, x1, y1, x2, y2):
    new_state = [row[:] for row in state]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

def misplaced_tiles(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != GOAL_STATE[i][j] and state[i][j] != 0:
                count += 1
    return count

def a_star_misplaced_tiles(start):
    open_list = []
    heapq.heappush(open_list, (0, start, 0, []))
    visited = set()

    while open_list:
        _, current, g, path = heapq.heappop(open_list)

        if current == GOAL_STATE:
            return path + [current]

        visited.add(tuple(map(tuple, current)))
        x, y = find_blank(current)
        moves = []
        if x > 0: moves.append(move_tile(current, x, y, x-1, y))
        if x < 2: moves.append(move_tile(current, x, y, x+1, y))
        if y > 0: moves.append(move_tile(current, x, y, x, y-1))
        if y < 2: moves.append(move_tile(current, x, y, x, y+1))

        for move in moves:
            move_tuple = tuple(map(tuple, move))
            if move_tuple not in visited:
                h = misplaced_tiles(move)
                f = g + 1 + h
                heapq.heappush(open_list, (f, move, g + 1, path + [current]))

    return None

def get_input():
    print("Enter your 8-puzzle state (0 for blank):")
    state = []
    for i in range(3):
        row = list(map(int, input(f"Row {i+1}: ").split()))
        state.append(row)
    return state

initial_state = get_input()
solution = a_star_misplaced_tiles(initial_state)

if solution:
    print("Puzzle solved using A* (Misplaced Tiles)!")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No solution found.")
