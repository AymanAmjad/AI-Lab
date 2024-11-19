import re

class UnificationError(Exception):
    """Exception raised for errors during unification."""
    pass

def is_variable(x):
    """Check if the term is a variable (starts with a lowercase letter)."""
    return isinstance(x, str) and x[0].islower()

def unify(term1, term2, subst=None):
    """
    Perform unification of two terms with a given substitution.
    
    :param term1: First term (variable, constant, or compound term).
    :param term2: Second term (variable, constant, or compound term).
    :param subst: Current substitution dictionary.
    :return: A dictionary of substitutions if unification succeeds.
    """
    if subst is None:
        subst = {}

    # Apply the substitution to both terms
    term1 = substitute(term1, subst)
    term2 = substitute(term2, subst)

    if term1 == term2:
        # Terms are already equal
        return subst
    elif is_variable(term1):
        return unify_var(term1, term2, subst)
    elif is_variable(term2):
        return unify_var(term2, term1, subst)
    elif isinstance(term1, tuple) and isinstance(term2, tuple):
        if term1[0] != term2[0] or len(term1[1]) != len(term2[1]):
            raise UnificationError(f"Cannot unify {term1} with {term2}.")
        for arg1, arg2 in zip(term1[1], term2[1]):
            subst = unify(arg1, arg2, subst)
        return subst
    else:
        raise UnificationError(f"Cannot unify {term1} with {term2}.")

def unify_var(var, term, subst):
    """
    Unify a variable with a term.
    
    :param var: The variable.
    :param term: The term.
    :param subst: Current substitution dictionary.
    :return: Updated substitution dictionary.
    """
    if var in subst:
        return unify(subst[var], term, subst)
    elif term in subst:
        return unify(var, subst[term], subst)
    elif occurs_check(var, term):
        raise UnificationError(f"Occurs check failed for {var} and {term}.")
    else:
        subst[var] = term
        return subst

def occurs_check(var, term):
    """Check if a variable occurs in a term."""
    if var == term:
        return True
    elif isinstance(term, tuple):
        return any(occurs_check(var, t) for t in term[1])
    return False

def substitute(term, subst):
    """Apply substitutions to a term."""
    if is_variable(term):
        while term in subst:
            term = subst[term]
        return term
    elif isinstance(term, tuple):
        return (term[0], [substitute(t, subst) for t in term[1]])
    else:
        return term

def parse_term(input_str):
    """Parse a term from a string input."""
    input_str = input_str.strip()
    if '(' in input_str:
        match = re.match(r'(\w+)\((.+)\)', input_str)
        if not match:
            raise ValueError(f"Invalid term format: {input_str}")
        predicate = match.group(1)
        args = match.group(2).split(',')
        return (predicate, [parse_term(arg.strip()) for arg in args])
    else:
        return input_str

# Example usage with user input
if __name__ == "__main__":
    print('Enter the first expression (e.g., Eats(x, Apple)): ')
    term1_str = input().strip()
    print('Enter the second expression (e.g., Eats(Riya, y)): ')
    term2_str = input().strip()

    try:
        term1 = parse_term(term1_str)
        term2 = parse_term(term2_str)
        substitution = unify(term1, term2)
        print("Substitution:", substitution)
    except UnificationError as e:
        print("Unification failed:", e)
    except ValueError as ve:
        print("Invalid input format:", ve)
