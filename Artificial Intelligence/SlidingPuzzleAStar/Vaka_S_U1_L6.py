# Name:          Date:
import random
import time


class HeapPriorityQueue:

    def __init__(self):
        self.q = ["dummy"]  # we do not use index 0 for easy index calulation
        self.current = 1  # to make this object iterable

    def next(self):  # define what __next__ does
        if self.current >= len(self.q):
            self.current = 1  # to restart iteration later
            raise StopIteration

        out = self.q[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.q) == 1  # b/c index 0 is dummy

    def swap(self, a, b):
        self.q[a], self.q[b] = self.q[b], self.q[a]

    # Add a value to the heap_pq
    def push(self, value):
        self.q.append(value)
        self.heapUp(len(self.q) - 1)

    def heapUp(self, i):
        if i != 1:
            while self.q[i] < self.q[i // 2]:
                self.swap(i, i // 2)
                i //= 2
                if i == 1:
                    break

    # helper method for reheap and pop
    def heapDown(self, i, size):
        while i * 2 < size:
            mc = i * 2
            if (i * 2) + 1 < size and (self.q[i * 2] >= self.q[(i * 2) + 1]):
                mc = i * 2 + 1
            if self.q[i] > self.q[mc]:
                self.swap(i, mc)
            i = mc

    # make the queue as a min-heap
    def reheap(self):
        size = len(self.q)
        for i in range(size // 2 - 1, 0, -1):
            self.heapDown(i, size)

    # remove the min value (root of the heap)
    # return the removed value
    def pop(self):
        self.swap(1, -1)
        r = self.q.pop(-1)
        self.heapDown(1, len(self.q))
        return r

    # remove a value at the given index (assume index 0 is the root)
    # return the removed value
    def remove(self, index):
        if index == 0:
            self.pop()
            return
        index += 1
        self.swap(index, len(self.q) - 1)
        r = self.q.pop(-1)
        self.heapDown(1, len(self.q))
        if self.q[index] < self.q[index // 2]:
            self.heapUp(index)
        else:
            self.heapDown(index, len(self.q))
        return r

    def len(self):
        return len(self.q)


def inversion_count(new_state, width=4, n=4):
    even = (new_state.find('_') // n) % 2 == 1
    new_state = new_state.replace('_', '')
    inv = 0
    for i, j in enumerate(new_state):
        inv += sum(j > k for k in new_state[i + 1:])
    if n % 2 == 0 and even:
        return inv % 2 == 1
    else:
        return inv % 2 == 0


def check_inversion():
    t1 = inversion_count("_42135678", 3, 3)  # N=3
    f1 = inversion_count("21345678_", 3, 3)
    t2 = inversion_count("4123C98BDA765_EF", 4)  # N is default, N=4
    f2 = inversion_count("4123C98BDA765_FE", 4)
    return t1 and t2 and not (f1 or f2)


def getInitialState(sample, size):
    sample_list = list(sample)
    random.shuffle(sample_list)
    new_state = ''.join(sample_list)
    while not inversion_count(new_state, size, size):
        random.shuffle(sample_list)
        new_state = ''.join(sample_list)
    return new_state


def swap(n, i, j):
    t = list(n)
    t[i], t[j] = t[j], t[i]
    return ''.join(t)


'''Generate a list which hold all children of the current state
   and return the list'''


def generate_children(state, size=4):
    t = []
    i = state.index("_")
    if (i % size) != 0:
        t.append(swap(state, i, i - 1))
    if (i % size) != (size - 1):
        t.append(swap(state, i, i + 1))
    if i >= size:
        t.append(swap(state, i, i - size))
    if i < (size * (size - 1)):
        t.append(swap(state, i, i + size))
    return t


def display_path(path_list, size):
    for n in range(size):
        for path in path_list:
            print(path[n * size:(n + 1) * size], end=" " * size)
        print()
    print("\nThe shortest path length is :", len(path_list))
    return ""


''' You can make multiple heuristic functions '''


def dist_heuristic(state, goal="_123456789ABCDEF", size=4):
    h = 0
    for i, v in enumerate(state):
        if v != '_':
            v = int(v, 16)
            h += abs(v % size - i % size) + abs(v // size - i // size)
    return h


def check_heuristic():
    a = dist_heuristic("152349678_ABCDEF", "_123456789ABCDEF", 4)
    b = dist_heuristic("8936C_24A71FDB5E", "_123456789ABCDEF", 4)
    return a < b


def a_star(start, goal="_123456789ABCDEF", h=dist_heuristic, size=4):
    nodes = HeapPriorityQueue()
    nodes.push((h(start), [start], start))
    vis = set()
    while not nodes.isEmpty():
        cr = nodes.pop()
        vis.add(cr[2])
        if cr[2] == goal:
            return cr[1]
        for child in generate_children(cr[2], size):
            if child not in vis:
                nodes.push((len(cr[1]) + h(child), cr[1] + [child], child))
                print(len(cr[1]) + h(child), child)
    return None


def bswap(i, j, state):
    state[i], state[j] = state[j], state[i]
    return state


def incMan(state, prev, cur, goal="_123456789ABCDEF", size=4):
    return (abs(state % size - prev % size) + abs(state // size - prev // size)) - (
                abs(state % size - cur % size) + abs(state // size - cur // size))


def solve(start, goal="_123456789ABCDEF", heur=incMan, size=4):
    lookup = [(1, 4),
              (0, 2, 5),
              (1, 3, 6),
              (2, 7),
              (0, 5, 8),
              (1, 4, 6, 9),
              (2, 5, 7, 10),
              (3, 6, 11),
              (4, 9, 12),
              (5, 8, 10, 13),
              (6, 9, 11, 14),
              (7, 10, 15),
              (8, 13),
              (12, 9, 14),
              (13, 10, 15),
              (11, 14)]
    nodes = HeapPriorityQueue()
    nodes.push((dist_heuristic(start), dist_heuristic(start), start, [start]))
    vis = set()
    while not nodes.isEmpty():
        cr = nodes.pop()
        vis.add(cr[2])
        if cr[2] == goal:
            return cr[3]
        i = cr[2].index("_")
        state = list(cr[2])
        for k, child in enumerate([''.join(bswap(i, j, state.copy())) for j in lookup[i]]):
            if child not in vis:
                h = cr[1] + heur(int(state[lookup[i][k]], 16), i, lookup[i][k])
                nodes.push((len(cr[3]) + h, h, child, cr[3] + [child]))
    return None


def main():
    # A star
    print("Inversion works?:", check_inversion())
    print("Heuristic works?:", check_heuristic())
    # initial_state = getInitialState("_123456789ABCDEF", 4)
    initial_state = input("Type initial state: ")
    if inversion_count(initial_state):
        cur_time = time.time()
        #path = a_star(initial_state)
        path = solve(initial_state)
        if path is not None:
            display_path(path, 4)
        else:
            print("No Path Found.")
        print("Duration: ", (time.time() - cur_time))
    else:
        print("{} did not pass inversion test.".format(initial_state))


if __name__ == '__main__':
    main()
