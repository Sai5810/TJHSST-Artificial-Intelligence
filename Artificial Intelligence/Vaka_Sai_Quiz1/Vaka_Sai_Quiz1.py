def valid(assignment, p, dist):
    if not assignment:
        td = {p}
    else:
        td = set()
        for k, v in assignment.items():
            d = abs(v - p)
            if d in dist:
                return None
            else:
                td.add(d)
    return td


def rec(assignment, dom, pos, dist):
    for d in dom:
        if d not in assignment:
            uv = d
            break
    else:
        return assignment
    for p in pos:
        if p not in assignment.values():
            td = valid(assignment, p, dist)
            if td is not None:
                assignment[uv] = p
                result = rec(assignment, dom, pos, set.union(dist, td))
                if result is not None:
                    print(result)
    return None


def main():
    print(rec({}, ["A", "B", "C", "D", "T"], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], set()))


if __name__ == '__main__':
    main()
