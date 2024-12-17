def minimax(node, depth, alpha, beta, maximizing_player, tree, static_eval, log, pruned_nodes):
    """
    Minimax with Alpha-Beta Pruning.
    Prunes all remaining child nodes once alpha >= beta becomes true.

    Args:
    - node: Current node being evaluated.
    - depth: Remaining depth to explore.
    - alpha: Alpha value for pruning.
    - beta: Beta value for pruning.
    - maximizing_player: True for MAX, False for MIN.
    - tree: The game tree represented as a dictionary.
    - static_eval: Function to evaluate leaf nodes.
    - log: List to log exploration and pruning details.
    - pruned_nodes: List to store pruned child nodes.

    Returns:
    - The evaluation value of the current node.
    """
    # Base case: If depth == 0 or terminal node
    if depth == 0 or node not in tree:
        return static_eval(node)

    if maximizing_player:  # Maximizing player
        max_eval = -float('inf')
        for idx, child in enumerate(tree[node]):
            eval_value = minimax(child, depth - 1, alpha, beta, False, tree, static_eval, log, pruned_nodes)
            max_eval = max(max_eval, eval_value)
            alpha = max(alpha, max_eval)

            # Log the decision process
            log.append({
                "Node": node,
                "Child": child,
                "Alpha": alpha,
                "Beta": beta,
                "Pruned": False
            })

            # Prune remaining siblings
            if alpha >= beta:
                pruned_nodes.extend(tree[node][idx + 1:])  # Log all remaining siblings as pruned
                log.append({
                    "Node": node,
                    "Child": child,
                    "Alpha": alpha,
                    "Beta": beta,
                    "Pruned": True
                })
                break
        return max_eval

    else:  # Minimizing player
        min_eval = float('inf')
        for idx, child in enumerate(tree[node]):
            eval_value = minimax(child, depth - 1, alpha, beta, True, tree, static_eval, log, pruned_nodes)
            min_eval = min(min_eval, eval_value)
            beta = min(beta, min_eval)

            # Log the decision process
            log.append({
                "Node": node,
                "Child": child,
                "Alpha": alpha,
                "Beta": beta,
                "Pruned": False
            })

            # Prune remaining siblings
            if alpha >= beta:
                pruned_nodes.extend(tree[node][idx + 1:])  # Log all remaining siblings as pruned
                log.append({
                    "Node": node,
                    "Child": child,
                    "Alpha": alpha,
                    "Beta": beta,
                    "Pruned": True
                })
                break
        return min_eval


# Static evaluation function for leaf nodes (returns the node value directly)
def static_evaluation(node):
    return node  # Assuming leaf nodes are represented as numerical values


# Example Game Tree
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [10, 9],
    'E': [14, 18],
    'F': [5, 4],
    'G': [50, 3]
}

# Initialize variables
log = []  # To store logs
pruned_nodes = []  # To track pruned nodes
root = 'A'  # Root of the game tree
depth = 3  # Depth limit

# Run Minimax with Alpha-Beta Pruning
root_value = minimax(root, depth, -float('inf'), float('inf'), True, tree, static_evaluation, log, pruned_nodes)

# Output Results
print(f"Value of the root node: {root_value}\n")

print("Alpha-Beta Log:")
for entry in log:
    print(entry)

print("\nPruned Nodes:")
print(pruned_nodes)
