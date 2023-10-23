import random


def getInitialState():
    x = "_12345678"
    l1 = list(x)
    random.shuffle(l1)
    y = ''.join(l1)
    return y


'''precondition: i<j
   swap characters at position i and j and return the new state'''


def swap(s, i, j):
    t = list(s)
    t[i], t[j] = t[j], t[i]
    return ''.join(t)


'''Generate a list which hold all children of the current state
   and return the list'''


def generate_children(state):
    t = []
    i = state.index("_")
    if i + 3 < 9:
        t.append(swap(state, i, i + 3))
    if i - 3 >= 0:
        t.append(swap(state, i, i - 3))
    if i + 1 < 9 and (i + 1) % 3 != 0:
        t.append(swap(state, i, i + 1))
    if i - 1 >= 0 and (i - 1) % 3 != 2:
        t.append(swap(state, i, i - 1))
    return t


def display_path(n, explored):  # key: current, value: parent
    l = []
    while explored[n] != "s":  # "s" is initial's parent
        l.append(n)
        n = explored[n]
    print()
    l = l[::-1]
    for i in l:
        print(i[0:3], end="   ")
    print()
    for j in l:
        print(j[3:6], end="   ")
    print()
    for k in l:
        print(k[6:9], end="   ")
    print("\n\nThe shortest path length is :", len(l))
    return ""


'''Find the shortest path to the goal state "_12345678" and
   returns the path by calling display_path() function to print all steps.
   You can make other helper methods, but you must use dictionary for explored.'''


def BFS(initial):
    exp = {initial: "s"}
    q = [initial]
    while q:
        c = q.pop(0)
        if c == "_12345678":
            return display_path(c, exp)
        for a in generate_children(c):
            if a not in exp:
                exp[a] = c
                q.append(a)
    return "No solution"


def DFS(initial):
    exp = {initial: "s"}
    stk = [initial]
    while stk:
        c = stk.pop()
        if c == "_12345678":
            return display_path(c, exp)
        for a in generate_children(c):
            if a not in exp:
                exp[a] = c
                stk.append(a)
    """Your code goes here"""
    return "No solution"


def main():
    #initial = getInitialState()
    initial = "84765231_"
    print("BFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    print(BFS(initial))
    print("DFS start with:\n", initial[0:3], "\n", initial[3:6], "\n", initial[6:], "\n")
    print(DFS(initial))


if __name__ == '__main__':
    main()
