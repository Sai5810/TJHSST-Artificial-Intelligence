import sys; args = sys.argv[1:]
import re
import math


def display(crossword):
    for i in crossword:
        print(''.join(i))


def dfs(start, crossword, row, col):
    st = [start]
    vis = set()
    while st:
        v = st.pop()
        if v not in vis and crossword[v[0]][v[1]] != '#':
            vis.add(v)
            if v[0] - 1 >= 0:
                st.append((v[0] - 1, v[1]))
            if v[0] + 1 < row:
                st.append((v[0] + 1, v[1]))
            if v[1] - 1 >= 0:
                st.append((v[0], v[1] - 1))
            if v[1] + 1 < col:
                st.append((v[0], v[1] + 1))
    return len(vis)


def backtrack(crossword, bsquare, i, j, row, col):
    print(bsquare)
    if bsquare < 2:
        for i, r in enumerate(crossword):
            for j, ch in enumerate(r):
                if ch != '#':
                    vislen = dfs((i, j), crossword, row, col)
                    empctr = 0
                    for rw in crossword:
                        empctr += sum(1 for i in rw if i != '#')
                    if vislen == empctr:
                        return 1
                    else:
                        return None
        return 1
    while i < row:
        while j < col:
            if crossword[i][j] == '-' and crossword[row - i - 1][col - j - 1] == '-':
                crossword[i][j] = '#'
                crossword[row - i - 1][col - j - 1] = '#'
                checkre = [''.join(crossword[i]), ''.join(k[j] for k in crossword), ''.join(crossword[row - i - 1]),
                           ''.join(k[col - j - 1] for k in crossword)]
                if not any(re.search(r'#-{1,2}#|^-{1,2}#|#-{1,2}$', k) for k in checkre):
                    if backtrack(crossword, bsquare - 2, i, j, row, col) is None:
                        crossword[i][j] = '-'
                        crossword[row - i - 1][col - j - 1] = '-'
                    else:
                        return 1
                else:
                    crossword[i][j] = '-'
                    crossword[row - i - 1][col - j - 1] = '-'
            j += 1
        i += 1
        j = 0


def checkhorz(x, crossword, bsquare):
    st = -1
    for i, ch in enumerate(crossword[x]):
        if ch == '#':
            if st != -1 and 1 <= i - st <= 2:
                for j in range(st + 1, i):
                    crossword[x][j] = '#'
                    bsquare = checkvert(j, crossword, bsquare - 1)
            st = i
    return bsquare


def checkvert(y, crossword, bsquare):
    st = -1
    for i, ch in enumerate(k[y] for k in crossword):
        if ch == '#':
            if st != -1 and 1 <= i - st <= 2:
                for j in range(st + 1, i):
                    crossword[j][y] = '#'
                    bsquare = checkhorz(j, crossword, bsquare - 1)
            st = i
    return bsquare


def main():
    seedstr = []
    dicfile = ''
    bsquare = 0
    row = 0
    col = 0
    for arg in args:
        if re.search(r'.*\.txt', arg):
            dicfile = arg
        elif re.search(r'^\d+x\d+$', arg):
            row, col = (int(i) for i in arg.split('x'))
        elif re.search(r'^\d+$', arg):
            bsquare = int(arg)
        else:
            cur = re.findall(r"[^\d\s]+|\d+", arg[1:])
            seedstr.append([int(cur[0]), int(cur[2]), arg[0], '#' if len(cur) < 4 else cur[3]])
    print(dicfile, row, col, bsquare, seedstr)
    crossword = [['-'] * col for _ in range(row)]
    for ss in seedstr:
        if ss[2] == 'H':
            tj = ss[1]
            for c in ss[3]:
                crossword[ss[0]][tj] = c
                tj += 1
        else:
            ti = ss[0]
            for c in ss[3]:
                crossword[ti][ss[1]] = c
                ti += 1
    opp = []
    for i, r in enumerate(crossword):
        for j, ch in enumerate(r):
            if ch == '#':
                bsquare -= 1
                if crossword[row - i - 1][col - j - 1] == '-':
                    opp.append((row - i - 1, col - j - 1))
                    bsquare -= 1
    for i, j in opp:
        crossword[i][j] = '#'
    if bsquare % 2 == 1:
        crossword[math.floor(row / 2)][math.floor(col / 2)] = '#'
    for i, r in enumerate(crossword):
        st = -1
        for j, ch in enumerate(r):
            if ch == '#':
                if st != -1 and 1 <= j - st <= 2:
                    for k in range(st + 1, j):
                        crossword[i][k] = '#'
                        bsquare = checkvert(k, crossword, bsquare - 1)
                st = j
    i = 0
    for c in zip(*crossword):
        st = -1
        for j, ch in enumerate(c):
            if ch == '#':
                if st != -1 and 1 <= j - st <= 2:
                    for k in range(st + 1, j):
                        crossword[k][i] = '#'
                        bsquare = checkhorz(k, crossword, bsquare - 1)
                st = j
        i += 1
    display(crossword)
    if bsquare < row * col:
        backtrack(crossword, bsquare, 0, 0, row, col)
    else:
        crossword = [['#'] * col for _ in range(row)]
    display(crossword)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
