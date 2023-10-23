import sys;

args = sys.argv[1:]
import re
import math
from timeit import default_timer as timer


def display(crossword):
    for i in crossword:
        print(''.join(i))


def dfs(start, crossword, row, col):
    stk = [start]
    vis = set()
    while stk:
        cr = stk.pop()
        if cr not in vis and crossword[cr[0]][cr[1]] != '#':
            vis.add(cr)
            if cr[0] - 1 >= 0:
                stk.append((cr[0] - 1, cr[1]))
            if cr[0] + 1 < row:
                stk.append((cr[0] + 1, cr[1]))
            if cr[1] - 1 >= 0:
                stk.append((cr[0], cr[1] - 1))
            if cr[1] + 1 < col:
                stk.append((cr[0], cr[1] + 1))
    return len(vis)


def check_connect(crossword, row, col):
    for i, r in enumerate(crossword):
        for j, ch in enumerate(r):
            if ch != '#':
                vis_len = dfs((i, j), crossword, row, col)
                emp_ctr = 0
                for rw in crossword:
                    emp_ctr += sum(1 for i in rw if i != '#')
                return vis_len == emp_ctr


def check3word(crossword):
    for r in crossword:
        if re.search(r'#[^#\s]{1,2}#|^[^#\s]{1,2}#|#[^#\s]{1,2}$', ''.join(r)):
            return False
    for c in zip(*crossword):
        if re.search(r'#[^#\s]{1,2}#|^[^#\s]{1,2}#|#[^#\s]{1,2}$', ''.join(c)):
            return False
    return True


# def repair_holes():

def backtrack(crossword, block, i, j, row, col):
    if block < 2:
        if check3word(crossword) and check_connect(crossword, row, col):
            return 1
        else:
            return None
    extra = []
    while i < row:
        while j < col:
            if crossword[i][j] == '-' and crossword[row - i - 1][col - j - 1] == '-':
                crossword[i][j] = '#'
                crossword[row - i - 1][col - j - 1] = '#'
                if not check3word(crossword):
                    extra.append([i, j])
                    crossword[i][j] = '-'
                    crossword[row - i - 1][col - j - 1] = '-'
                elif backtrack(crossword, block - 2, i, j, row, col) is None:
                    crossword[i][j] = '-'
                    crossword[row - i - 1][col - j - 1] = '-'
                else:
                    return 1
            j += 1
        i += 1
        j = 0
    for i, j in extra:
        crossword[i][j] = '#'
        crossword[row - i - 1][col - j - 1] = '#'
        if backtrack(crossword, block - 2, i, j, row, col) is None:
            crossword[i][j] = '-'
            crossword[row - i - 1][col - j - 1] = '-'
        else:
            return 1


def main():
    t = timer()
    seeds, dict_file, block, row, col = [], '', 0, 0, 0
    for arg in args:
        if re.search(r'.*\.txt', arg):
            dict_file = arg
        elif re.search(r'^\d+x\d+$', arg):
            row, col = (int(i) for i in arg.split('x'))
        elif re.search(r'^\d+$', arg):
            block = int(arg)
        else:
            cur = re.findall(r"[^\d\s]+|\d+", arg[1:])
            seeds.append([int(cur[0]), int(cur[2]), arg[0], '#' if len(cur) < 4 else cur[3]])
    crossword = [['-'] * col for _ in range(row)]
    for seed in seeds:
        if seed[2] == 'H' or seed[2] == 'h':
            tj = seed[1]
            for c in seed[3]:
                crossword[seed[0]][tj] = c
                tj += 1
        else:
            ti = seed[0]
            for c in seed[3]:
                crossword[ti][seed[1]] = c
                ti += 1
    opp = []
    for i, r in enumerate(crossword):
        for j, ch in enumerate(r):
            if ch == '#':
                block -= 1
                if crossword[row - i - 1][col - j - 1] == '-':
                    opp.append((row - i - 1, col - j - 1))
                    block -= 1
    for i, j in opp:
        crossword[i][j] = '#'
    if block % 2 == 1:
        crossword[math.floor(row / 2)][math.floor(col / 2)] = '#'
    if block < row * col:
        backtrack(crossword, block, 0, 0, row, col)
    else:
        crossword = [['#'] * col for _ in range(row)]
    display(crossword)
    print(timer() - t)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
