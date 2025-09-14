# Import Pretty Print
# Import DPLL Func
from pprint import pprint
from DPLL import dpll


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
        for var in sorted(result):
            print(f"x{var} = {result[var]}")


if __name__ == "__main__":
    main()
