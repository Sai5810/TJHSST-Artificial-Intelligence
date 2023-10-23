import sys;

args = sys.argv[1:]
file = open(args[0], 'r')
import math
import random


def activate(afc, x):
    if afc == 'T1':
        return x
    elif afc == 'T2':
        return x if x > 0 else 0
    elif afc == 'T3':
        return 1 / (1 + math.exp(-x))
    elif afc == 'T4':
        return 2 / (1 + math.exp(-x)) - 1


def activ_der(afc, y):
    if afc == 'T1':
        return 1
    elif afc == 'T2':
        return 1 if y > 0 else 0
    elif afc == 'T3':
        return y * (1 - y)
    elif afc == 'T4':
        return .5 * (y + 1) * (1 - y)


def ff(x0, weights, layer_ct, afc):
    nodes = [x0]
    for idx, wl in enumerate(weights[:-1]):
        for idx2 in range(layer_ct[idx + 1]):
            print(nodes[idx], wl[idx2::layer_ct[idx + 1]])
        nodes.append([activate(afc, dot(nodes[idx], wl[idx2::layer_ct[idx + 1]])) for idx2 in range(layer_ct[idx + 1])])
    return nodes + [[i * j for i, j in zip(nodes[-1], weights[-1])]]


def dot(x, y):
    return sum(i * j for i, j in zip(x, y))


def bp(layer_ct, targets, x_nodes, weights, act_func, alpha):
    e_nodes = [[t - j for t, j in zip(targets, x_nodes[-1])]]
    e_weights = [[x * e for x, e in zip(x_nodes[-2], e_nodes[0])]]
    e_nodes.append([en * ew * activ_der(act_func, x) for en, ew, x in zip(e_nodes[0], weights[-1], x_nodes[-2])])
    e_nodes, e_weights, weights = [[0.23433374494070847, -1.0647657235555499],
                                   [0.1031009171735046, -0.4667908892932805]], [
                                      [0.09967857829042859, -0.6263679812479411]], [
                                      [1.18, -0.23, -0.66, -1.89, 0.64, 1.17, 0.99, -0.79, 0.24, 0.22, -0.53, -0.31],
                                      [-1.6, -0.26, 0.64, 1.47, 0.25,
                                       -0.34], [1.8, 1.81]]

    for idx, wi in enumerate(weights[:-1][::-1]):
        sl = []
        for e in e_nodes[idx + 1]:
            for x in x_nodes[-idx - 3]:
                sl.append(x * e)
        e_weights.append(sl)
        print(wi[0::layer_ct[-idx - 3]])
        e_nodes.append(
            [dot(wi[idx2::layer_ct[-idx - 3]], e_nodes[-1]) * activ_der(act_func, x)
             for idx2, x in enumerate(x_nodes[-idx - 3])])

    print([[0.23433374494070847, -1.0647657235555499], [0.1031009171735046, -0.4667908892932805],
           [-0.15627107659557052, -0.03491672423766387, 0.0476961912374434], [-0.0, -0.011165884662304084, 0.0, 0.0]])
    return [[ew * alpha + w for ew, w in zip(ew_l, w_l)] for ew_l, w_l in zip(e_weights[::-1], weights)]


def main():
    inputs, targets = [], []
    bias = 1
    act_func = 'T3'
    for line in file:
        i, t = line.split('=>')
        inputs.append([float(v) for v in i.split()] + [bias])
        targets.append([float(v) for v in t.split()])
    layer_ct = [len(inputs[0]), len(targets[0]) + 1, len(targets[0]), len(targets[0])]
    err = 1000
    weights = []
    num_weights = sum(val * layer_ct[idx] for idx, val in enumerate(layer_ct[1:]))
    while err > num_weights / 13:
        weights = [[round(random.uniform(-2.0, 2.0), 2) for _ in range(layer_ct[i] * layer_ct[i + 1])] for i in
                   range(len(layer_ct) - 2)] + [[round(random.uniform(-2.0, 2.0), 2) for _ in range(layer_ct[-1])]]
        err = 0
        for inp, target in zip(inputs, targets):
            nodes = ff(inp.copy(), weights, layer_ct, act_func)
            err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2
    alpha = .1
    prev_err = err
    for i in range(700000):
        if i % 1000 == 0:
            err = 0
            for inp, target in zip(inputs, targets):
                nodes = ff(inp.copy(), weights, layer_ct, act_func)
                err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2
            if err < .01:
                break
            if prev_err - err < .0001:
                err = 100
                while err > num_weights / 13:
                    weights = [[round(random.uniform(-2.0, 2.0), 2) for _ in range(layer_ct[i] * layer_ct[i + 1])] for i
                               in range(len(layer_ct) - 2)] + [
                                  [round(random.uniform(-2.0, 2.0), 2) for _ in range(layer_ct[-1])]]
                    err = 0
                    for inp, target in zip(inputs, targets):
                        nodes = ff(inp.copy(), weights, layer_ct, act_func)
                        err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2
            prev_err = err
        inp, target = list(zip(inputs, targets))[0]
        weights = [[1.18, -0.23, -0.66, -1.89, 0.64, 1.17, 0.99, -0.79, 0.24, 0.22, -0.53, -0.31],
                   [-1.6, -0.26, 0.64, 1.47, 0.25, -0.34], [1.8, 1.81]]
        print(weights, inp)
        nodes = ff(inp.copy(), weights, layer_ct, act_func)
        print(nodes)
        weights = bp(layer_ct, target, nodes, weights, act_func, alpha)
    err = 0
    for inp, target in zip(inputs, targets):
        nodes = ff(inp.copy(), weights, layer_ct, act_func)
        err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2
    print('Layer Counts:', *layer_ct)
    print('Weights:')
    for w in weights:
        print(*w)
    print('Error:', err)


if __name__ == '__main__':
    main()
# Sai Vaka, Period 5, 2023
