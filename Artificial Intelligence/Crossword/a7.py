import sys; args = sys.argv[1:]
myLines = open(args[0], "r").read().splitlines()
import re
import math


def init(seeds, dic, block, row, col, word_freq):
    for line in myLines:
        line = line.rstrip()
        if len(line) > 2:
            if len(line) not in dic:
                dic[len(line)] = {line}
            else:
                dic[len(line)].add(line)
            for idx, ch in enumerate(line):
                word_tuple = (idx, ch, len(line))
                if word_tuple in word_freq:
                    word_freq[word_tuple] += 1
                else:
                    word_freq[word_tuple] = 0
    for arg in args[1:]:
        if re.search(r'^\d+x\d+$', arg):
            row, col = (int(i) for i in arg.split('x'))
        elif re.search(r'^\d+$', arg):
            block = int(arg)
        else:
            cur = re.findall(r"[^\d\s]+|\d+", arg[1:])
            seeds.append([int(cur[0]), int(cur[2]), arg[0], '#' if len(cur) < 4 else cur[3].lower()])
    return seeds, dic, block, row, col, word_freq


def fix(seeds, block, row, col):
    crossword = [['-'] * col for _ in range(row)]
    opp = {(math.floor(row / 2), math.floor(col / 2))} if block % 2 == 1 else set()
    for seed in seeds:
        if seed[2] == 'H' or seed[2] == 'h':
            tj = seed[1]
            for c in seed[3]:
                crossword[seed[0]][tj] = c
                if c == '#':
                    block -= 1
                    opp.add((row - seed[0] - 1, col - tj - 1))
                tj += 1
        else:
            ti = seed[0]
            for c in seed[3]:
                crossword[ti][seed[1]] = c
                if c == '#':
                    block -= 1
                    opp.add((row - ti - 1, col - seed[1] - 1))
                ti += 1
    for i, j in opp:
        if crossword[i][j] != '#':
            crossword[i][j] = '#'
            block -= 1
    crossword = ['#' * (col + 2)] + ['#' + ''.join(i) + '#' for i in crossword] + ['#' * (col + 2)]
    crossword, temp = fill_holes(crossword)
    block -= temp
    crossword, temp = fill_components(crossword)
    block -= temp
    return crossword, block


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


def is_connected(crossword):
    for i, r in enumerate(crossword[1:-1]):
        for j, ch in enumerate(r[1:-1]):
            if ch != '#':
                vis_len = len(dfs((i + 1, j + 1), crossword))
                emp_ctr = sum(sum(i != '#' for i in rw) for rw in crossword)
                return vis_len == emp_ctr


def fill_components(crossword):
    sblock = sum(i.count('#') for i in crossword)
    vis_list = []
    for i, r in enumerate(crossword[1:-1]):
        for j, ch in enumerate(r[1:-1]):
            if ch != '#' and not any(((i + 1, j + 1) in vis) for vis in vis_list):
                vis_list.append(dfs((i + 1, j + 1), crossword))
    vis_list = sorted(vis_list, key=len, reverse=True)
    crossword = [list(i) for i in crossword]
    for i in vis_list[1:]:
        for j, k in i:
            crossword[j][k] = '#'
    return [''.join(i) for i in crossword], sum(i.count('#') for i in crossword) - sblock


def transpose(crossword):
    return [''.join(i[j] for i in crossword) for j, _ in enumerate(crossword[0])]


def hole_rec(crossword):
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
        crossword = transpose(hole_rec(transpose(crossword)))
    return crossword


def fill_holes(crossword):
    sblock = sum(i.count('#') for i in crossword)
    crossword = hole_rec(crossword)
    crossword = transpose(hole_rec(transpose(crossword)))
    fblock = sum(i.count('#') for i in crossword)
    return crossword, fblock - sblock


def block_comp(i, j, crossword, row, col):
    left = 0
    idx = j
    while idx >= 0 and crossword[i][idx] != '#':
        left += 1
        idx -= 1
    right = 0
    idx = j
    while idx < col and crossword[i][idx] != '#':
        right += 1
        idx += 1
    top = 0
    idx = i
    while idx >= 0 and crossword[idx][j] != '#':
        top += 1
        idx -= 1
    bot = 0
    idx = i
    while idx < row and crossword[idx][j] != '#':
        bot += 1
        idx += 1
    return left * right + top * bot


def create(crossword, block, row, col):
    if block < 2:
        return is_connected(crossword)
    pos = []
    for i in range(1, len(crossword) - 1):
        for j in range(1, len(crossword[i]) - 1):
            if crossword[i][j] == '-' and crossword[row - i + 1][col - j + 1] == '-':
                pos.append((i, j))
    pos.sort(key=lambda x: block_comp(x[0], x[1], crossword, row, col))
    for i, j in pos:
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
            temp, blockg = fill_holes(temp)
            if block - blockg - 2 >= 0:
                test = create(temp, block - blockg - 2, row, col)
                if test != False:
                    if test == True:
                        return temp
                    else:
                        return test
    return False


def empty_comp(dic, cur, word_freq):
    score = len(dic[len(cur)])
    alp_ct = 0
    for i, ch in enumerate(cur):
        if ch.isalpha():
            alp_ct += 1
            word_tup = (i, ch, len(cur))
            if word_tup not in word_freq:
                return 0
            if alp_ct == 1:
                score = word_freq[word_tup]
            else:
                score = min(word_freq[word_tup], score) / 2
    return score


def get_empties(crossword):
    empty = []
    for i, r in enumerate(crossword):
        for m in re.finditer('(?<=#)[^#]+(?=#)|^[^#]+(?=#)|(?<=#)[^#]+$|^[^#]+$', r):
            cur = m[0]
            if '-' in cur:
                empty.append([i, m.start(), cur, 'h'])
    for j, c in enumerate(zip(*crossword)):
        c = ''.join(c)
        for m in re.finditer('(?<=#)[^#]+(?=#)|^[^#]+(?=#)|(?<=#)[^#]+$|^[^#]+$', c):
            cur = m[0]
            if '-' in cur:
                empty.append([m.start(), j, cur, 'v'])
    return empty


def find_ver(crossword, i, j, row):
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


def find_horz(crossword, i, j, col):
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


def freq_comp(word_freq, word):
    total = 0
    for index, character in enumerate(word):
        total += word_freq[(index, character, len(word))]
    return total


def check_hors(i, j, temp, dic, col, pattern):
    for idx in range(i, i + len(pattern)):
        cur = find_horz(temp, idx, j, col)[1].replace('-', '.')
        for word in dic[len(cur)]:
            if re.match(cur, word):
                break
        else:
            return False
    return True


def check_verts(i, j, temp, dic, row, pattern):
    for idx in range(j, j + len(pattern)):
        cur = find_ver(temp, i, idx, row)[1].replace('-', '.')
        for word in dic[len(cur)]:
            if re.match(cur, word):
                break
        else:
            return False
    return True


def solve(crossword, row, col, dic, vis, word_freq):
    for i in crossword:
        print(i)
    print()
    empty = sorted(get_empties(crossword), key=lambda x: empty_comp(dic, x[2], word_freq))
    if not empty:
        return crossword
    else:
        i, j, pattern, vh = empty[0]
        pattern = pattern.replace('-', '.')
        words = []
        for word in dic[len(pattern)]:
            if word not in vis and re.match(pattern, word):
                words.append(word)
        words.sort(key=lambda x: freq_comp(word_freq, x), reverse=True)
        if vh == 'v':
            for word in words:
                temp = [list(x) for x in crossword]
                for k, val in enumerate(word):
                    temp[k + i][j] = val
                temp = [''.join(x) for x in temp]
                if check_hors(i, j, temp, dic, col, pattern):
                    vis2 = vis.copy()
                    vis2.add(word)
                    res = solve(temp, row, col, dic, vis2, word_freq)
                    if res is not None:
                        return res
        else:
            for word in words:
                temp = [x for x in crossword]
                temp[i] = temp[i][:j] + word + temp[i][j + len(word):]
                if check_verts(i, j, temp, dic, row, pattern):
                    vis2 = vis.copy()
                    vis2.add(word)
                    res = solve(temp, row, col, dic, vis2, word_freq)
                    if res is not None:
                        return res


def main():
    seeds, dic, block, row, col, word_freq = init([], {}, 0, 0, 0, {})
    if block >= row * col:
        for _ in range(row):
            print('#' * col)
    else:
        crossword, block = fix(seeds, block, row, col)
        if block > 0:
            crossword = create(crossword, block, row, col)
        crossword = [i[1:-1] for i in crossword[1:-1]]
        crossword = solve(crossword, row, col, dic, set(), word_freq)
        for i in crossword:
            print(i)


if __name__ == '__main__':
    main()

# Sai Vaka, 5, 2023
