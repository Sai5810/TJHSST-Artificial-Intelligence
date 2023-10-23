import sys; args = sys.argv[1:]
myLines = open(args[0], "r").read().splitlines()
import re
import math


def init(seeds, dic, block, row, col, wordFreq):
    for line in myLines:
        line = line.rstrip()
        if len(line) > 2 and line.isalpha():
            if len(line) not in dic:
                dic[len(line)] = {line}
            else:
                dic[len(line)].add(line)
            for idx, ch in enumerate(line):
                wordTuple = (idx, ch, len(line))
                if wordTuple in wordFreq:
                    wordFreq[wordTuple] += 1
                else:
                    wordFreq[wordTuple] = 0
    for arg in args[1:]:
        if re.search(r'^\d+x\d+$', arg):
            row, col = (int(i) for i in arg.split('x'))
        elif re.search(r'^\d+$', arg):
            block = int(arg)
        else:
            cur = re.findall(r"[^\d\s]+|\d+", arg[1:])
            seeds.append([int(cur[0]), int(cur[2]), arg[0], '#' if len(cur) < 4 else cur[3].lower()])
    return seeds, dic, block, row, col, wordFreq


def fix(seeds, block, row, col):
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
    return crossword


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


def getEmpties(crossword, dic):
    empty = []
    for i, r in enumerate(crossword):
        for m in re.finditer('(?<=#)[^#]+(?=#)|^[^#]+(?=#)|(?<=#)[^#]+$|^[^#]+$', r):
            cur = m[0]
            if '-' in cur:
                score = len(dic[len(cur)])
                alpCt = sum(c.isalpha() for c in cur)
                if alpCt > 0:
                    score /= 5 * alpCt
                empty.append([score, i, m.start(), cur, 'h'])
    for j, c in enumerate(zip(*crossword)):
        c = ''.join(c)
        for m in re.finditer('(?<=#)[^#]+(?=#)|^[^#]+(?=#)|(?<=#)[^#]+$|^[^#]+$', c):
            cur = m[0]
            if '-' in cur:
                score = len(dic[len(cur)])
                alpCt = sum(c.isalpha() for c in cur)
                if alpCt > 0:
                    score /= 5 * alpCt
                empty.append([score, m.start(), j, cur, 'v'])
    return sorted(empty)


def findVer(crossword, i, j, row):
    i2 = i
    front = []
    while i2 >= 0 and crossword[i2][j] != '#':
        front.append(crossword[i2][j])
        i2 -= 1
    start = i2 + 1
    i2 = i + 1
    back = []
    while i2 < row and crossword[i2][j] != '#':
        back.append(crossword[i2][j])
        i2 += 1
    return start, (''.join(front[::-1]) + ''.join(back))


def findHorz(crossword, i, j, col):
    j2 = j
    front = []
    while j2 >= 0 and crossword[i][j2] != '#':
        front.append(crossword[i][j2])
        j2 -= 1
    start = j2 + 1
    j2 = j + 1
    back = []
    while j2 < col and crossword[i][j2] != '#':
        back.append(crossword[i][j2])
        j2 += 1
    return start, (''.join(front[::-1]) + ''.join(back))


def heuristic(wordFreq, word):
    total = 0
    for index, character in enumerate(word):
        total += wordFreq[(index, character, len(word))]
    return total


def solve(crossword, row, col, dic, vis, wordFreq):
    # for i in crossword:
    #     print(i)
    # print()
    empty = getEmpties(crossword, dic)
    if not empty:
        return crossword
    else:
        i, j, pattern, vh = empty[0][1:]
        pattern = pattern.replace('-', '.')
        possibleWords = []
        for word in dic[len(pattern)]:
            if word not in vis and re.match(pattern, word):
                possibleWords.append(word)
        possibleWords.sort(key=lambda w: heuristic(wordFreq, w), reverse=True)
        if vh == 'v':
            for word in possibleWords:
                temp = [list(x) for x in crossword]
                for k, val in enumerate(word):
                    temp[k + i][j] = val
                temp = [''.join(x) for x in temp]
                if not any('-' in sublist for sublist in temp):
                    ctr = 0
                    for idx in range(i, i + len(pattern)):
                        cur = findHorz(temp, idx, j, col)[1]
                        if cur in dic[len(cur)]:
                            ctr += 1
                    if ctr != len(pattern):
                        continue
                visC = vis.copy()
                visC.add(word)
                res = solve(temp, row, col, dic, visC, wordFreq)
                if res is not None:
                    return res
        else:
            for word in possibleWords:
                temp = [x for x in crossword]
                temp[i] = temp[i][:j] + word + temp[i][j + len(word) + 1:]
                if not any('-' in sublist for sublist in temp):
                    ctr = 0
                    for idx in range(j, j + len(pattern)):
                        cur = findVer(temp, i, idx, row)[1]
                        if cur in dic[len(cur)]:
                            ctr += 1
                    if ctr != len(pattern):
                        continue
                visC = vis.copy()
                visC.add(word)
                res = solve(temp, row, col, dic, visC, wordFreq)
                if res is not None:
                    return res


def main():
    seeds, dic, block, row, col, wordFreq = init([], {}, 0, 0, 0, {})
    if block >= row * col:
        for _ in range(row):
            print('#' * col)
    else:
        crossword = fix(seeds, block, row, col)
        if block > 0:
            crossword = create(crossword, block, 0, 0, row, col)
        crossword = [i[1:-1] for i in crossword[1:-1]]
        for i in crossword:
            print(i)
        crossword = solve(crossword, row, col, dic, set(), wordFreq)
        for i in crossword:
            print(i)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
