from time import perf_counter

insets = []


def rec(assignment, adj):
    for d in range(20):
        if d not in assignment and not bool(assignment & adj[d]):
            a1 = assignment.copy()
            a1.add(d)
            insets.append(a1)
            rec(a1, adj)


def main():
    t_start = perf_counter()
    adj = {0: {1, 10, 19},
           1: {0, 8, 2},
           2: {1, 3, 6},
           3: {2, 19, 4},
           4: {5, 3, 17},
           5: {4, 6, 15},
           6: {2, 5, 7},
           7: {6, 8, 14},
           8: {1, 9, 7},
           9: {10, 13, 8},
           10: {0, 9, 11},
           11: {10, 18, 12},
           12: {16, 11, 13},
           13: {12, 14, 9},
           14: {15, 7, 13},
           15: {16, 5, 14},
           16: {17, 12, 15},
           17: {16, 4, 18},
           18: {11, 17, 19},
           19: {0, 3, 18}}
    rec(set(), adj)
    print(max(insets, key=len))
    print(f'Time Elapsed: {perf_counter() - t_start}')


if __name__ == '__main__':
    main()
