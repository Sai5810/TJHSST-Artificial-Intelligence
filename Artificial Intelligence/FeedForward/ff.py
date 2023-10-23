import sys; args = sys.argv[1:]
file = open(args[0], 'r')
import math


def transfer(t_func, x):
    if t_func == 'T1':
        return x
    elif t_func == 'T2':
        return x if x > 0 else 0
    elif t_func == 'T3':
        return 1 / (1 + math.exp(-x))
    elif t_func == 'T4':
        return 2 / (1 + math.exp(-x)) - 1


def evalu(file, inp, t_func):
    weights = [[float(i) for i in line.split()] for line in file]
    for wl in weights[:-1]:
        nex = []
        tot = 0
        idx = 0
        for w in wl:
            tot += w * inp[idx]
            idx += 1
            if idx >= len(inp):
                idx = 0
                nex.append(transfer(t_func, tot))
                tot = 0
        inp = nex
    return [i * j for i, j in zip(inp, weights[-1])]


def main():
    inputs, t_func, transfer_found = [], 'T1', False
    for arg in args[1:]:
        if not transfer_found:
            t_func, transfer_found = arg, True
        else:
            inputs.append(float(arg))
    for x in evalu(file, inputs, t_func):
        print(x, end=' ')


if __name__ == '__main__':
    main()
# Sai Vaka, Period 5, 2023
