# Alpha-Beta Pruning Implementation

def alpha_beta_pruning(node, depth, alpha, beta, maximizing_player, tree, log):
    """
    Alpha-Beta Pruning Algorithm to find root value and track pruned subtrees.
    
    Args:
    - node: Current node being evaluated.
    - depth: Depth of the current node in the game tree.
    - alpha: Current alpha value.
    - beta: Current beta value.
    - maximizing_player: True if the node is a MAX node, False for MIN.
    - tree: The game tree represented as a dictionary (node: [children]).
    - log: A list to store the alpha-beta values and pruned subtrees.

    Returns:
    - The value of the node.
    """
    # Leaf node: Return its value
    if node not in tree:
        return node  # Leaf nodes are represented by their values
    
    # Initialize best value
    if maximizing_player:
        best = -float('inf')
    else:
        best = float('inf')

    # Traverse children
    for child in tree[node]:
        # Call recursively for children with flipped maximizing/minimizing role
        if maximizing_player:
            val = alpha_beta_pruning(child, depth + 1, alpha, beta, False, tree, log)
            best = max(best, val)
            alpha = max(alpha, best)
        else:
            val = alpha_beta_pruning(child, depth + 1, alpha, beta, True, tree, log)
            best = min(best, val)
            beta = min(beta, best)

        # Log the alpha-beta updates
        log.append({
            "Node": node,
            "Child": child,
            "Alpha": alpha,
            "Beta": beta,
            "Pruned": beta <= alpha
        })

        # Prune
        if beta <= alpha:
            break

    return best


# Example Game Tree
# Representing a tree where 'A' is the root and leaves are numerical values.
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [3, 5],
    'E': [6, 9],
    'F': [1, 2],
    'G': [0, -1]
}

# Running the Alpha-Beta Pruning Algorithm
log = []  # To store logs
root_value = alpha_beta_pruning('A', 0, -float('inf'), float('inf'), True, tree, log)

# Display Results
print(f"Value of the root node: {root_value}")
print("\nAlpha-Beta Log:")
for entry in log:
    print(entry)
