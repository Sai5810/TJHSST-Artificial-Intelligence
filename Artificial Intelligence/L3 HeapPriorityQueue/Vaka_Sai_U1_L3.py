# Name: Sai Vaka
# Date: 9/24/21

import random


class HeapPriorityQueue:

    def __init__(self):
        self.queue = ["dummy"]  # we do not use index 0 for easy index calulation
        self.current = 1  # to make this object iterable

    def next(self):  # define what __next__ does
        if self.current >= len(self.queue):
            self.current = 1  # to restart iteration later
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 1  # b/c index 0 is dummy

    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

    # Add a value to the heap_pq
    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)

    def heapUp(self, i):
        if i != 1:
            while self.queue[i] < self.queue[i // 2]:
                self.swap(i, i // 2)
                i //= 2
                if i == 1:
                    break

    # helper method for reheap and pop
    def heapDown(self, i, size):
        while i * 2 < size:
            mc = i * 2
            if (i * 2) + 1 < size and (self.queue[i * 2] >= self.queue[(i * 2) + 1]):
                mc = i * 2 + 1
            if self.queue[i] > self.queue[mc]:
                self.swap(i, mc)
            i = mc

    # make the queue as a min-heap
    def reheap(self):
        size = len(self.queue)
        for i in range(size // 2 - 1, 0, -1):
            self.heapDown(i, size)

    # remove the min value (root of the heap)
    # return the removed value
    def pop(self):
        self.swap(1, -1)
        r = self.queue.pop(-1)
        self.heapDown(1, len(self.queue))
        return r

    # remove a value at the given index (assume index 0 is the root)
    # return the removed value
    def remove(self, index):
        index += 1
        self.swap(index, len(self.queue) - 1)
        r = self.queue.pop(-1)
        self.heapDown(1, len(self.queue))
        if self.queue[index] < self.queue[index // 2]:
            self.heapUp(index)
        else:
            self.heapDown(index, len(self.queue))
        return r


# This method is for testing. Do not change it.
def isHeap(heap, k):
    left, right = 2 * k, 2 * k + 1
    if left == len(heap):
        return True
    elif len(heap) == right and heap[k] > heap[left]:
        return False
    elif right < len(heap):
        if heap[k] > heap[left] or heap[k] > heap[right]:
            return False
        else:
            return isHeap(heap, left) and isHeap(heap, right)
    return True


# This method is for testing. Do not change it.
def main():
    pq = HeapPriorityQueue()  # create a HeapPriorityQueue object
    print("Check if dummy 0 is still dummy:", pq.queue[0])
    # assign random integers into the pq
    '''for i in range(20):
        t = random.randint(10, 99)
        print(t, end=" ")
        pq.push(t)'''
    for i in [79, 35, 35, 56, 87, 34, 69, 41, 51, 55, 81, 76, 46, 38, 38, 79, 40, 37, 48, 94]:
        print(i, end=" ")
        pq.push(i)
    print()
    # print the pq which is a min-heap
    for x in pq:
        print(x, end=" ")
    print()
    # remove test
    print("Index 4 is removed:", pq.remove(4))
    # check if pq is a min-heap
    for x in pq:
        print(x, end=" ")
    print("\nIs a min-heap?", isHeap(pq.queue, 1))
    temp = []
    while not pq.isEmpty():
        temp.append(pq.pop())
        print(temp[-1], end=" ")
    print("\nIn ascending order?", temp == sorted(temp))


if __name__ == '__main__':
    main()
