import sys;

args = sys.argv[1:]
import re
import math


def display(crossword):
    for i in crossword:
        print(i)


def dfs(start, crossword):
    stk = [start]
    vis = set()
    while stk:
        cr = stk.pop()
        if cr not in vis and crossword[cr[0]][cr[1]] != '#':
            vis.add(cr)
            stk.append((cr[0] - 1, cr[1]))
            stk.append((cr[0] + 1, cr[1]))
            stk.append((cr[0], cr[1] - 1))
            stk.append((cr[0], cr[1] + 1))
    return vis


def isConnected(crossword):
    for i, r in enumerate(crossword[1:-1]):
        for j, ch in enumerate(r[1:-1]):
            if ch != '#':
                vis_len = len(dfs((i + 1, j + 1), crossword))
                emp_ctr = sum(sum(i != '#' for i in rw) for rw in crossword)
                return vis_len == emp_ctr


def fillComponents(crossword):
    sblock = sum(i.count('#') for i in crossword)
    visList = []
    for i, r in enumerate(crossword[1:-1]):
        for j, ch in enumerate(r[1:-1]):
            if ch != '#' and not any(((i + 1, j + 1) in vis) for vis in visList):
                visList.append(dfs((i + 1, j + 1), crossword))
    visList = sorted(visList, key=len, reverse=True)
    crossword = [list(i) for i in crossword]
    for i in visList[1:]:
        for j, k in i:
            crossword[j][k] = '#'
    return [''.join(i) for i in crossword], sum(i.count('#') for i in crossword) - sblock


def transpose(crossword):
    return [''.join(i[j] for i in crossword) for j, _ in enumerate(crossword[0])]


def holeRec(crossword):
    rep = 0
    for i, j in enumerate(crossword):
        crossword[i], cr = re.subn('#-#', '###', crossword[i])
        rep += cr
        crossword[i], cr = re.subn('#--#', '####', crossword[i])
        rep += cr
        crossword[i], cr = re.subn('#-#', '###', crossword[i])
        rep += cr
        crossword[i], cr = re.subn('#--#', '####', crossword[i])
        rep += cr
    if rep > 0:
        crossword = transpose(holeRec(transpose(crossword)))
    return crossword


def fillHoles(crossword):
    sblock = sum(i.count('#') for i in crossword)
    crossword = holeRec(crossword)
    crossword = transpose(holeRec(transpose(crossword)))
    fblock = sum(i.count('#') for i in crossword)
    return crossword, fblock - sblock


def create(crossword, block, i, j, row, col):
    if block < 2:
        return isConnected(crossword)
    while i < row + 1:
        while j < col + 1:
            if crossword[i][j] == '-' and crossword[row - i + 1][col - j + 1] == '-':
                temp = [x for x in crossword]
                t2 = list(temp[i])
                t2[j] = '#'
                temp[i] = ''.join(t2)
                t2 = list(temp[row - i + 1])
                t2[col - j + 1] = '#'
                temp[row - i + 1] = ''.join(t2)
                checkre = [temp[i], temp[row - i + 1], ''.join(k[j] for k in temp),
                           ''.join(k[col - j + 1] for k in temp)]
                if not any(re.search(r'#[^\s#-]#|#[^\s#-][^#]#|#[^#][^\s#-]#', k) for k in checkre):
                    temp, blockg = fillHoles(temp)
                    if block - blockg - 2 >= 0:
                        test = create(temp, block - blockg - 2, i, j, row, col)
                        if test != False:
                            if test == True:
                                return temp
                            else:
                                return test
            j += 1
        i += 1
        j = 0
    return False

# def fillVert():


# def solve(crossword, dic, row, col):
#     for rIdx, r in enumerate(crossword):
#         j = 0
#         while j < len(r):
#             if r[j] != '#':
#                 ori = r
#                 rL = list(r)
#                 empty = [rL[j]]
#                 stJ = j
#                 j += 1
#                 while j < len(r) and rL[j] != '#' :
#                     empty.append(rL[j])
#                     j += 1
#                 if '-' in empty:
#                     for word in dic[len(empty)]:
#                         for i, ch in enumerate(word):
#                             if rL[i] != '-' and ch != rL[i]:
#                                 break
#                         else:
#                             for i in range(stJ, stJ + len(word)):
#                                 rL[i] = word[i]
#                                 # fill the vertical as well
#
#             j += 1
#     return crossword

    #get all empty words
    #choose based on already filled words and


def main():
    seeds, dic, block, row, col = [], {}, 0, 0, 0
    for arg in args:
        if re.search(r'.*\.txt', arg):
            with open(arg) as file:
                while line := file.readline():
                    line = line.rstrip()
                    if len(line) > 2 and line.isalpha():
                        if len(line) not in dic:
                            dic[len(line)] = {line}
                        else:
                            dic[len(line)].add(line)
        elif re.search(r'^\d+x\d+$', arg):
            row, col = (int(i) for i in arg.split('x'))
        elif re.search(r'^\d+$', arg):
            block = int(arg)
        else:
            cur = re.findall(r"[^\d\s]+|\d+", arg[1:])
            seeds.append([int(cur[0]), int(cur[2]), arg[0], '#' if len(cur) < 4 else cur[3]])
    # initialize values
    if block >= row * col:
        for _ in range(row):
            print('#' * col)
    else:
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
        crossword = ['#' * (col + 2)] + ['#' + ''.join(i) + '#' for i in crossword] + ['#' * (col + 2)]
        crossword, temp = fillHoles(crossword)
        block -= temp
        crossword, temp = fillComponents(crossword)
        block -= temp
        # fix to make cw rotationally symmetric, 3-word, and connected
        if block > 0:
            crossword = create(crossword, block, 1, 1, row, col)
        crossword = [i[1:-1] for i in crossword[1:-1]]
        display(crossword)
        # create grid
        # crossword = solve(crossword, dic, row, col)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
