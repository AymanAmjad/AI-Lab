import numpy as np
import time

# Define the objective function for the N-Queens problem
def queens_max(position):
    queen_not_attacking = 0

    # Compare each pair of queens to check if they are attacking each other
    for i in range(len(position) - 1):
        no_attack_on_j = 0
        for j in range(i + 1, len(position)):
            # Check for no horizontal or diagonal attacks
            if (position[j] != position[i]) and (position[j] != position[i] + (j - i)) and (position[j] != position[i] - (j - i)):
                no_attack_on_j += 1
                if no_attack_on_j == len(position) - 1 - i:
                    queen_not_attacking += 1

    # Add 1 if all queens are not attacking each other, meaning we solved the problem
    if queen_not_attacking == len(position) - 1:
        queen_not_attacking += 1
    return queen_not_attacking

# Function to perform simulated annealing
def simulated_annealing(queens_max, length, max_iters=500, temp=1.0, cooling_rate=0.99):
    # Initialize position and best position
    position = np.random.permutation(length)
    best_position = position.copy()
    best_objective = queens_max(position)

    for iteration in range(max_iters):
        # Temperature decay
        temp *= cooling_rate

        # Create a neighbor by swapping two random positions
        i, j = np.random.randint(0, length, size=2)
        neighbor_position = position.copy()
        neighbor_position[i], neighbor_position[j] = neighbor_position[j], neighbor_position[i]

        # Calculate objective for the neighbor
        neighbor_objective = queens_max(neighbor_position)

        # Print the current state
        print(f"Iteration {iteration + 1}:")
        print(f"  Current Position: {position}")
        print(f"  Neighbor Position: {neighbor_position}")
        print(f"  Objective Value: {neighbor_objective}")
        print(f"  Temperature: {temp:.4f}")
        print("-" * 50)
        time.sleep(0.25)  # Pause for half a second to make changes more visible

        # Decide if we should move to the neighbor
        if neighbor_objective > best_objective or np.random.rand() < np.exp((neighbor_objective - best_objective) / temp):
            position = neighbor_position
            best_objective = neighbor_objective
            best_position = position.copy()

        # Stop if we find a solution
        if best_objective == length:
            break

    return best_position, best_objective

# Define problem parameters
length = 8  # Number of queens / board size
max_iters = 500
temp = 1.0
cooling_rate = 0.90

# Run simulated annealing
best_position, best_objective = simulated_annealing(queens_max, length, max_iters, temp, cooling_rate)

print('The best position found is:', best_position)
print('The number of queens that are not attacking each other is:', best_objective)
