import sys; args = sys.argv[1:]
puzzles = open(args[0], "r").read().splitlines()
import time

# puzzles = open("puzzles.txt", "r").read().splitlines()


def solve(puzzle, neighbors):
    # q_table is quantity table {'1': number of value '1' occurred, ...}
    domain = {i: '123456789' for i, v in enumerate(puzzle) if v == '.'}
    for i, v in enumerate(puzzle):
        if v != '.':
            for j in neighbors[i]:
                if j in domain and v in domain[j]:
                    domain[j] = domain[j].replace(v, '')
    return recursive_backtracking(list(puzzle), neighbors, domain)


# optional helper function: you are allowed to change it
def recursive_backtracking(assignment, neighbors, domain):
    try:
        var = min(domain.items(), key=lambda x: len(x[1]))[0]
    except ValueError:
        return ''.join(assignment)
    for val in domain[var]:
        a1 = assignment.copy()
        a1[var] = val
        d1 = domain.copy()
        del d1[var]
        for j in neighbors[var]:
            if j in d1 and val in d1[j]:
                d1[j] = d1[j].replace(val, '')
        result = recursive_backtracking(a1, neighbors, d1)
        if result is not None:
            assignment = a1.copy()
            domain = d1.copy()
            return result


def sudoku_csp(n=9):
    return [[]]


def sudoku_neighbors(csp_table):  # {0:[0, 1, 2, 3, 4, ...., 8, 9, 18, 27, 10, 11, 19, 20], 1:
    csp_table = [{0, 1, 2, 9, 10, 11, 18, 19, 20}, {3, 4, 5, 12, 13, 14, 21, 22, 23}, {6, 7, 8, 15, 16, 17, 24, 25, 26},
                 {27, 28, 29, 36, 37, 38, 45, 46, 47}, {30, 31, 32, 39, 40, 41, 48, 49, 50},
                 {33, 34, 35, 42, 43, 44, 51, 52, 53}, {54, 55, 56, 63, 64, 65, 72, 73, 74},
                 {57, 58, 59, 66, 67, 68, 75, 76, 77}, {60, 61, 62, 69, 70, 71, 78, 79, 80}]
    ret = {}
    for var in range(0, 81):
        for i, v in enumerate(csp_table):
            if var in v:
                ret[var] = v.copy()
                break
        for i in range((var // 9) * 9, ((var // 9) * 9) + 9):
            ret[var].add(i)
        for i in range(var % 9, 81, 9):
            ret[var].add(i)
        ret[var].remove(var)
    return ret


# sum of all ascii code of each char - (length of the solution * ascii code of min char)
def checksum(solution):
    return sum(ord(i) for i in solution) - (len(solution) * ord(min(solution)))


def main():
    csp_table = sudoku_csp()  # rows, cols, and sub_blocks
    neighbors = sudoku_neighbors(
        csp_table)  # each position p has its neighbors {p:[positions in same row/col/subblock], ...}
    start_time = time.time()
    for line, puzzle in enumerate(puzzles):
        line, puzzle = line + 1, puzzle.rstrip()
        print(f"{line}: {puzzle}")
        solution = solve(puzzle, neighbors)
        if solution is None:
            print("No solution found.")
            break
        print(f'{" " * (len(str(line)) + 2)}{solution} {checksum(solution)}')
    print("Duration:", (time.time() - start_time))


if __name__ == '__main__': main()
# Sai Vaka, Period 5, 2023
