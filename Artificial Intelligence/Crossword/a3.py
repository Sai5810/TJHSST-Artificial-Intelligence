import sys; args = sys.argv[1:]
import re
import math
# from timeit import default_timer as timer


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


def checkhorz(x, crossword, block):
    st = -1
    for i, ch in enumerate(crossword[x]):
        if ch == '#':
            if st != -1 and 1 <= i - st - 1 <= 2:
                for j in range(st + 1, i):
                    crossword[x][j] = '#'
                    block = checkvert(j, crossword, block - 1)
            st = i
    return block


def checkvert(y, crossword, block):
    st = -1
    for i, ch in enumerate(k[y] for k in crossword):
        if ch == '#':
            if st != -1 and 1 <= i - st - 1 <= 2:
                for j in range(st + 1, i):
                    crossword[j][y] = '#'
                    block = checkhorz(j, crossword, block - 1)
            st = i
    return block


def repair_holes(crossword, block, row, col):
    for i, r in enumerate(crossword):
        st = -1
        for j, ch in enumerate(r):
            if ch == '#':
                if st != -1 and 1 <= j - st - 1 <= 2:
                    for k in range(st + 1, j):
                        crossword[i][k] = '#'
                        block = checkvert(k, crossword, block - 1)
                        if crossword[row - i - 1][col - k - 1] == '-':
                            crossword[row - i - 1][col - k - 1] = '#'
                            block = checkvert(col - k - 1, crossword, block - 1)
                st = j
                if 1 <= st <= 2:
                    for k in range(0, st):
                        crossword[i][k] = '#'
                        block = checkvert(k, crossword, block - 1)
                        if crossword[row - i - 1][col - k - 1] == '-':
                            crossword[row - i - 1][col - k - 1] = '#'
                            block = checkvert(col - k - 1, crossword, block - 1)
        if row - 3 <= st <= row - 2:
            for k in range(st, row):
                crossword[i][k] = '#'
                block = checkvert(k, crossword, block - 1)
                if crossword[row - i - 1][col - k - 1] == '-':
                    crossword[row - i - 1][col - k - 1] = '#'
                    block = checkvert(col - k - 1, crossword, block - 1)
    i = 0
    for c in zip(*crossword):
        st = -1
        for j, ch in enumerate(c):
            if ch == '#':
                if st != -1 and 1 <= j - st - 1 <= 2:
                    for k in range(st + 1, j):
                        crossword[k][i] = '#'
                        block = checkhorz(k, crossword, block - 1)
                        if crossword[row - k - 1][col - i - 1] == '-':
                            crossword[row - k - 1][col - i - 1] = '#'
                            block = checkhorz(row - k - 1, crossword, block - 1)
                st = j
                if 1 <= st <= 2:
                    for k in range(0, st):
                        crossword[k][i] = '#'
                        block = checkhorz(k, crossword, block - 1)
                        if crossword[row - k - 1][col - i - 1] == '-':
                            crossword[row - k - 1][col - i - 1] = '#'
                            block = checkhorz(row - k - 1, crossword, block - 1)
        if col - 3 <= st <= col - 2:
            for k in range(st, col):
                crossword[k][i] = '#'
                block = checkhorz(k, crossword, block - 1)
                if crossword[row - k - 1][col - i - 1] == '-':
                    crossword[row - k - 1][col - i - 1] = '#'
                    block = checkhorz(row - k - 1, crossword, block - 1)
        i += 1
    return block


def backtrack(crossword, block, i, j, row, col):
    if block < 2:
        return check_connect(crossword, row, col)
    while i < row:
        while j < col:
            if crossword[i][j] == '-' and crossword[row - i - 1][col - j - 1] == '-':
                temp = [x[:] for x in crossword]
                temp[i][j] = '#'
                temp[row - i - 1][col - j - 1] = '#'
                tblock = repair_holes(temp, block - 2, row, col)
                if tblock >= 0:
                    test = backtrack(temp, tblock, i, j, row, col)
                    if test != False:
                        # display(temp)
                        # print()
                        if test == True:
                            return temp
                        else:
                            return test
            j += 1
        i += 1
        j = 0
    return False


def main():
    # t = timer()
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
    opp = [(math.floor(row / 2), math.floor(col / 2))] if block % 2 == 1 else []
    for seed in seeds:
        if seed[2] == 'H' or seed[2] == 'h':
            tj = seed[1]
            for c in seed[3]:
                crossword[seed[0]][tj] = c
                if c == '#':
                    block -= 1
                    opp.append((row - seed[0] - 1, col - tj - 1))
                tj += 1
        else:
            ti = seed[0]
            for c in seed[3]:
                crossword[ti][seed[1]] = c
                if c == '#':
                    block -= 1
                    opp.append((row - ti - 1, col - seed[1] - 1))
                ti += 1
    for i, j in opp:
        if crossword[i][j] != '#':
            crossword[i][j] = '#'
            block -= 1
    if block < row * col:
        block = repair_holes(crossword, block, row, col)
        crossword = backtrack(crossword, block, 0, 0, row, col)
    else:
        crossword = [['#'] * col for _ in range(row)]
    display(crossword)
    # print(timer() - t)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
