def CDCL(clauses, num_vars):
    # state
    assign = [0] * (num_vars + 1)   # assignment: 0=unassigned, 1=true, -1=false
    level = [0] * (num_vars + 1)    # decision level
    ante = [None] * (num_vars + 1)  # antecedent clause
    trail = []                      # assignment trail
    trail_limits = []               # indices where decision levels start
    decision_level = 0

    # helpers
    def literal_value(lit):
        val = assign[abs(lit)]
        if val == 0: return 0
        return val if lit > 0 else -val

    def enqueue(lit, antecedent=None):
        var = abs(lit)
        val = 1 if lit > 0 else -1
        if assign[var] != 0:
            return assign[var] == val
        assign[var] = val
        level[var] = decision_level
        ante[var] = antecedent
        trail.append(lit)
        return True

    def propagate():
        i = 0
        while i < len(trail):
            lit = trail[i]
            i += 1
            for clause in clauses:
                if any(literal_value(l) == 1 for l in clause):
                    continue
                unassigned = [l for l in clause if literal_value(l) == 0]
                if not unassigned:
                    return clause
                if len(unassigned) == 1:
                    if not enqueue(unassigned[0], clause):
                        return clause
        return None

    def analyze_conflict(conflict):
        nonlocal decision_level
        learned = []
        involved = set(abs(l) for l in conflict)
        backtrack_level = 0
        for lit in reversed(trail):
            var = abs(lit)
            if var in involved:
                learned.append(-lit)
                if level[var] < decision_level:
                    backtrack_level = max(backtrack_level, level[var])
                involved.remove(var)
                if not involved:
                    break
                if ante[var]:
                    involved.update(abs(l) for l in ante[var])
        return learned, backtrack_level

    def backtrack(to_level):
        nonlocal decision_level
        while trail and level[abs(trail[-1])] > to_level:
            v = abs(trail.pop())
            assign[v] = 0
            ante[v] = None
            level[v] = 0
        decision_level = to_level
        while trail_limits and len(trail) < trail_limits[-1]:
            trail_limits.pop()

    def pick_branch_var():
        for v in range(1, num_vars + 1):
            if assign[v] == 0:
                return v
        return None

    # --- main loop ---
    confl = propagate()
    if confl:
        return False, {}

    while True:
        if all(assign[1:]):  # SAT
            # Build assignment dict
            model = {v: (assign[v] == 1) for v in range(1, num_vars + 1)}
            return True, model

        var = pick_branch_var()
        if var is None:  # all assigned
            model = {v: (assign[v] == 1) for v in range(1, num_vars + 1)}
            return True, model

        decision_level += 1
        trail_limits.append(len(trail))
        enqueue(var, None)

        while True:
            confl = propagate()
            if not confl:
                break
            if decision_level == 0:
                return False, {}
            learned, back_level = analyze_conflict(confl)
            clauses.append(learned)
            backtrack(back_level)
            if learned:
                enqueue(learned[0], learned)

    return False, {}   # safeguard
