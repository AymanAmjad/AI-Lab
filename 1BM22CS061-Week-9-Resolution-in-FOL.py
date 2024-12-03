import re
import collections
import itertools
import copy
import time
import queue

# Function to standardize variables
def standardization(sentence, variable_map, counter):
    sentence_list = list(sentence)
    for i in range(len(sentence_list)):
        if sentence_list[i] == ',' or sentence_list[i] == '(':
            if sentence_list[i+1].islower():
                if sentence_list[i+1] not in variable_map:
                    variable_map[sentence_list[i+1]] = f"var{counter}"
                    sentence_list[i+1] = f"var{counter}"
                    counter += 1
                else:
                    sentence_list[i+1] = variable_map[sentence_list[i+1]]
    return "".join(sentence_list), variable_map, counter

# Function to check if something is a variable
def is_variable(x):
    return isinstance(x, str) and x.islower()

# Function to perform unification
def unify(x, y, theta):
    if theta is None:
        return None
    elif x == y:
        return theta
    elif is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    else:
        return None

# Function to unify a variable with a term
def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    else:
        theta[var] = x
        return theta

# Function to negate a literal
def negate(literal):
    if literal[0] == '~':
        return literal[1:]
    else:
        return '~' + literal

# Function to substitute variables based on a substitution map
def substitute(expr, theta):
    if is_variable(expr):
        if expr in theta:
            return theta[expr]
        else:
            return expr
    else:
        return expr  # Handle compound terms here if necessary

# Resolves two clauses using unification
def resolve_clauses(clause1, clause2):
    for literal1 in clause1:
        for literal2 in clause2:
            theta = unify(literal1, negate(literal2), {})
            if theta is not None:
                new_clause = []
                for literal in clause1:
                    new_literal = substitute(literal, theta)
                    if new_literal not in new_clause and new_literal != negate(literal2):
                        new_clause.append(new_literal)
                for literal in clause2:
                    new_literal = substitute(literal, theta)
                    if new_literal not in new_clause and new_literal != literal2:
                        new_clause.append(new_literal)
                if not new_clause:  # If the clause is empty, return 'NIL'
                    return 'NIL'
                return new_clause
    return None

# Function to perform resolution on the KB and query
def resolve(kb, query):
    q = queue.Queue()
    q.put(query)
    processed_clauses = set()  # Track processed clauses to avoid duplicates

    while not q.empty():
        clause = q.get()
        clause_tuple = tuple(clause)  # Convert clause to a tuple for immutability
        if clause_tuple in processed_clauses:
            continue  # Skip this clause if it has already been processed
        processed_clauses.add(clause_tuple)

        # Check if the clause matches a literal in the KB
        for clause2 in kb:
            resolvent = resolve_clauses(clause, clause2)
            if resolvent == 'NIL':
                return True  # Found an empty clause, query is provable
            if resolvent is not None and tuple(resolvent) not in processed_clauses:
                q.put(resolvent)
    
    return False  # No empty clause found, query is not provable

# Negate the query and apply resolution
def prove_query(kb, query):
    # Negate the query (as per proof by contradiction)
    negated_query = negate(query)
    
    # Start the resolution process with the negated query
    if resolve(kb, [negated_query]):
        return False  # Query is not provable (since the negation is inconsistent)
    else:
        return True  # Query is provable (since negation led to a contradiction)

# Example KB and Queries
kb = {
    'Likes': {1: [["Likes(John, x)", "~Food(x)"]]},
    'Food': {1: [["Food(Apple)", "Food(Vegetables)", "Food(Peanuts)"]]},
    'Eats': {1: [["Eats(Anil, Peanuts)"]]},
    'Killed': {1: [["~Killed(Anil)"]]}
}

queries = ['Likes(John, Peanuts)']

# Run resolution for each query
for query in queries:
    if prove_query(kb, query):
        print(f"Query '{query}' is provable.")
    else:
        print(f"Query '{query}' is not provable.")
