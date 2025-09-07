# main.py
from pprint import pprint
from DPLL import dpll

# paste your dpll(...) function here

def main():
    # Example CNF: (x1 ∨ ¬x2) ∧ (¬x1 ∨ x3) ∧ (x2) ∧ (¬x3 ∨ x2)
    cnf = [
        [1, -2],
        [-1, 3],
        [2],
        [-3, 2]
    ]

    result = dpll(cnf)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE with assignment:")
        # pretty-print in order of variable index
        for var in sorted(result):
            print(f"x{var} = {result[var]}")

if __name__ == "__main__":
    main()
