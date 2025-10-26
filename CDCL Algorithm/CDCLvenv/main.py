from pysat.solvers import Solver

# (x1 OR x2) AND (NOT x1 OR x3)
sat_cnf = [[1, 2], [-1, 3]]

# (x1) AND (NOT x1)
unsat_cnf = [[1], [-1]]

# (x1) OR (NOT x2)
sat2_cnf = [[1, -2]]


#glucose3 is used as CDCL Sat Solver

print("First Clause")
with Solver(name='glucose3') as s:
    for clause in sat_cnf:
        s.add_clause(clause)
    
    if s.solve():
        print("SAT:")
        print(s.get_model())
    else:
        print("UNSAT")


    
print("\nSecond Clause")
with Solver(name='glucose3') as s:
    for clause in unsat_cnf:
        s.add_clause(clause)
    
    if s.solve():
        print("SAT:")
        print(s.get_model())
    else:
        print("UNSAT")



print("\nThird Clause")
with Solver(name='glucose3') as s:
    for clause in sat2_cnf:
        s.add_clause(clause)
    
    if s.solve():
        print("SAT:")
        print(s.get_model())
    else:
        print("UNSAT")