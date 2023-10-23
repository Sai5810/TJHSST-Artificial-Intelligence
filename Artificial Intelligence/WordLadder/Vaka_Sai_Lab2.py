from string import ascii_lowercase
from copy import deepcopy


def IDS(s, e, wdict, maxDepth):
    for i in range(1, maxDepth + 1):
        IDSres = rec(s, e, wdict, {s: ""}, i)
        if IDSres is not None:
            return trace(s, e, IDSres)


def trace(s, e, exp):
    path = [e]
    while path[-1] != s:
        path.append(exp[path[-1]])
    path.reverse()
    return path


def rec(s, e, wdict, exp, lim):
    if lim != 0:
        if s == e:
            return exp
        else:
            for a in wdict.get(s):
                if a not in exp:
                    exp[a] = s
                    res = rec(a, e, wdict, deepcopy(exp), lim - 1)
                    if res is not None:
                        return res


def rDLS(s, e, wdict, lim):
    return trace(s, e, rec(s, e, wdict, {s: ""}, lim - 1))


def BFS(s, e, wdict):
    exp = {s: ""}
    q = [s]
    while q:
        cr = q.pop(0)
        if cr == e:
            return trace(s, e, exp)
        for a in wdict.get(cr):
            if a not in exp:
                exp[a] = cr
                q.append(a)
    return ["No solution"], 0


words = set()
with open("words.txt") as file:
    while line := file.readline().rstrip():
        words.add(line)
wdict = {}
for w in words:
    wdict.update({w: []})
    for c in ascii_lowercase:
        for j in range(len(w)):
            nw = w[:j] + c + w[j + 1:]
            if nw != w and nw in words:
                wdict.get(w).append(nw)
bRes = BFS(input("Type the starting word: "), input("Type the goal word: "), wdict)
print(bRes)
print(f"The number of steps: {len(bRes)}")
lim = int(input("Type the limit (1 - 20): "))
s = input("Type the starting word: ")
e = input("Type the goal word: ")
rDLSres = rDLS(s, e, wdict, lim)
print(f'Path: {rDLSres}')
print(f"steps within {lim} limit: {len(rDLSres) + 1}")
IDSres = IDS(s, e, wdict, 20)
print(f'Shortest Path: {IDSres}')
print(f"Steps: {len(IDSres)}")
