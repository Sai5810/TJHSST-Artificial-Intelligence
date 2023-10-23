import time
from string import ascii_lowercase
from queue import PriorityQueue


def generate_adjacents(w, words):
    """ words_set is a set which has all words.
    By comparing current and words in the words_set,
    generate adjacents set of current and return it"""
    adj_set = set()
    for c in ascii_lowercase:
        for j in range(len(w)):
            if c != w[j]:
                nw = w[:j] + c + w[j + 1:]
                if nw in words:
                    adj_set.add(nw)
    return adj_set


def check_adj(words_set):
    # This check method is written for words_6_longer.txt
    adj = generate_adjacents('listen', words_set)
    target = {'listee', 'listel', 'litten', 'lister', 'listed'}
    return adj == target


def trace(s, e, exp):
    path = [e]
    while path[-1] != s:
        path.append(exp[path[-1]])
    path.reverse()
    return path


def bi_bfs(st, goal, words_set):
    '''The idea of bi-directional search is to run two simultaneous searches--
    one forward from the initial state and the other backward from the goal--
    hoping that the two searches meet in the middle.
    '''
    if st == goal:
        return []
    expF = {st: ""}
    expB = {goal: ""}
    qF = [st]
    qB = [goal]
    while qF and qB:
        crF = qF.pop(0)
        crB = qB.pop(0)
        for a in generate_adjacents(crF, words_set):
            if a not in expF:
                expF[a] = crF
                qF.append(a)
        for a in generate_adjacents(crB, words_set):
            if a not in expB:
                expB[a] = crB
                qB.append(a)
        for i in qF:
            for j in qB:
                if i == j:
                    return trace(st, i, expF)[:-1] + (trace(goal, j, expB))[::-1]
    return ["No solution"], 0


def heuristic(a, b):
    return sum(a[i] != b[i] for i in range(len(a)))


def a_star(st, goal, words_set):
    nodes = PriorityQueue()
    nodes.put((heuristic(st, goal), [st], st))
    vis = set()
    while not nodes.empty():
        cr = nodes.get()
        for i in nodes:
            print(i)
        vis.add(cr[2])
        if cr[2] == goal:
            return cr[1]
        for child in generate_adjacents(cr[2], words_set):
            if child not in vis:
                nodes.put((len(cr[1]) + heuristic(child, goal), cr[1] + [child], child))
    return None


def main():
    filename = input("Type the word file: ")
    words_set = set()
    file = open(filename, "r")
    for word in file.readlines():
        words_set.add(word.rstrip('\n'))
    print("Check generate_adjacents():", check_adj(words_set))
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    cur_time = time.time()
    #path = bi_bfs(initial, goal, words_set)
    path = a_star(initial, goal, words_set)
    if path is not None:
        print(path)
        print("The number of steps: ", len(path))
        print("Duration: ", time.time() - cur_time)
    else:
        print("There's no path")


if __name__ == '__main__':
    main()
