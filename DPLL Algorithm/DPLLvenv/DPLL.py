# formula = CNF Formual(List of clauses)
# assignment = Memory for variable states(True or False) for current branch
def dpll(formula, assignment=None):
    if assignment is None:  # Catering for Mutable Default argument
        assignment = {}

    # return the single literal in the clause, if the clause length = 1
    def unit_clauses(F):
        return [c[0] for c in F if len(c) == 1]

    # Count the number of literals in a single clause
    # If clause appears as only pos OR only neg, append
    def pure_literals(F):
        counts = {}
        for clause in F:
            for lit in clause:
                counts[lit] = counts.get(lit, 0) + 1
        pures = []
        for v in {abs(l) for l in counts}:
            if v in counts and -v not in counts:
                pures.append(v)
            elif -v in counts and v not in counts:
                pures.append(-v)
        return pures

    # Helper method for unit_clauses
    def simplify(F, lit):
        newF = []
        for clause in F:
            if lit in clause:
                continue  # Clause satisfied
            if -lit in clause:
                new_clause = [l for l in clause if l != -lit]
                if not new_clause:
                    return None  # Empty clause -> UNSAT
                newF.append(new_clause)
            else:
                newF.append(clause)
        return newF

    # Base Case for DPLL
    if not formula:
        return assignment  # SAT
    if any(len(c) == 0 for c in formula):
        return None  # UNSAT

    # Unit Propagation
    # The units are simplified and reduced to a single literal
    # unit_clauses loops over itself to ensure any new single literals are taken care of
    units = unit_clauses(formula)
    while units:
        for u in units:
            assignment[abs(u)] = (u > 0)
            formula = simplify(formula, u)
            if formula is None:
                return None
        units = unit_clauses(formula)
        if not formula:
            return assignment

    # Pure Literal Elimination
    # Similar to the above, remove any literals with a single polarity
    pures = pure_literals(formula)
    while pures:
        for p in pures:
            assignment[abs(p)] = (p > 0)
            formula = simplify(formula, p)
            if formula is None:
                return None
        pures = pure_literals(formula)
        if not formula:
            return assignment

    # Choose a decision variable and branch
    for clause in formula:
        for lit in clause:
            v = abs(lit)
            if v not in assignment:
                # Try v = True
                res = dpll(simplify(formula, v), {**assignment, v: True})
                if res is not None:
                    return res
                # Try v = False
                return dpll(simplify(formula, -v), {**assignment, v: False})

    # If all variables seen are assigned and no empty clause: SAT
    return assignment
