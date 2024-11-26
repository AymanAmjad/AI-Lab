# Define initial facts and rules
facts = {"InAmerica(West)", "SoldWeapons(West, Nono)", "Enemy(Nono, America)"}
rules = [
    {
        "conditions": ["InAmerica(x)", "SoldWeapons(x, y)", "Enemy(y, America)"],
        "conclusion": "Criminal(x)",
    },
    {
        "conditions": ["Enemy(y, America)"],
        "conclusion": "Dangerous(y)",
    },
]

# Forward chaining function
def forward_chaining(facts, rules):
    derived_facts = set(facts)  # Initialize derived facts
    while True:
        new_fact_found = False

        for rule in rules:
            # Create a list to store the facts that match the conditions of the rule
            matching_facts = []
            for condition in rule["conditions"]:
                for fact in derived_facts:
                    if condition in fact:  # Simple string match
                        matching_facts.append((condition, fact))

            # If all conditions of the rule are satisfied, derive the conclusion
            if len(matching_facts) == len(rule["conditions"]):
                # Now check if the conclusion of the rule is not already in the facts
                conclusion = rule["conclusion"]
                
                # Check if the conclusion contains variables and substitute them
                for condition, fact in matching_facts:
                    for var in ["x", "y"]:  # Loop through variables to substitute
                        if var in condition:
                            # Substitute variables in the conclusion
                            conclusion = conclusion.replace(var, fact.split("(")[1].split(")")[0])

                # Add the conclusion if it's not already present
                if conclusion not in derived_facts:
                    derived_facts.add(conclusion)
                    print(f"New fact derived: {conclusion}")
                    new_fact_found = True

        # Exit loop if no new fact is found
        if not new_fact_found:
            break

    return derived_facts

# Run forward chaining
final_facts = forward_chaining(facts, rules)
print("\nFinal derived facts:")
for fact in final_facts:
    print(fact)
