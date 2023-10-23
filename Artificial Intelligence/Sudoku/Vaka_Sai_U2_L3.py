import copy


def check_complete(assignment, csp_table):
    return True


def select_unassigned_var(assignment, variables, csp_table):
    return 0


def ordered_domain(var_index, assignment, variables, csp_table):
    return []


def update_variables(value, var_index, assignment, variables, csp_table):
    return {}


def recursive_backtracking(assignment, variables, csp_table):
    return None


def sudoku_csp():
    return [[]]


def initial_variables(puzzle, csp_table):
    return {}


def isValid(val, var, assignment, variables, csp_table):
    csp_table = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
                 {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50},
                 {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
                 {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]
    for i, v in enumerate(csp_table):
        if var in v:
            for j in v:
                if j != var and assignment[j] == val:
                    return False
            break
    for i in range((var // 9) * 9, ((var // 9) * 9) + 9):
        if i != var and assignment[i] == val:
            return False
    for i in range(var % 9, 81, 9):
        if i != var and assignment[i] == val:
            return False
    return True


def recursive_backtracking(assignment, variables, csp_table):
    try:
        var = assignment.index('.')
    except ValueError:
        return ''.join(assignment)
    for val in range(1, 10):
        val = str(val)
        if isValid(val, var, assignment, 1, csp_table):
            a1 = copy.deepcopy(assignment)
            a1[var] = val
            result = recursive_backtracking(a1, 1, csp_table)
            if result is not None:
                assignment[var] = val
                return result


def backtracking_search(puzzle, variables, csp_table):
    csp_table = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
                 {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50},
                 {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
                 {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]
    return recursive_backtracking(list(puzzle), 1, csp_table)


def display(solution):
    ret = "-" * 19 + "\n"
    for i in range(0, len(solution), 9):
        if i % 27 == 0 and i != 0:
            ret += "\n"
        for j in range(i, i + 9, 3):
            ret += " ".join(solution[j:j + 3]) + "  "
        ret += "\n"
    ret += "-" * 19
    return ret


def main():
    puzzle = input("Type a 81-char string:")
    while len(puzzle) != 81:
        print("Invalid puzzle")
        puzzle = input("Type a 81-char string: ")
    csp_table = sudoku_csp()
    variables = initial_variables(puzzle, csp_table)
    print("Initial:\n" + display(puzzle))
    solution = backtracking_search(puzzle, variables, csp_table)
    if solution is not None:
        print("solution\n" + display(solution))
    else:
        print("No solution found.\n")


if __name__ == '__main__':
    main()
# Sai Vaka, Period 5, 2023