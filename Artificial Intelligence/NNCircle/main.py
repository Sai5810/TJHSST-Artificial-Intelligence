import sys; args = sys.argv[1:]
import math
import random
import time

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


def ff(x0, weights, afc):
    nodes = [x0]
    for wl in weights[:-1]:
        nex = []
        tot = 0
        idx = 0
        for w in wl:
            tot += w * x0[idx]
            idx += 1
            if idx >= len(x0):
                idx = 0
                nex.append(activate(afc, tot))
                tot = 0
        nodes.append(nex)
        x0 = nex
    return nodes + [[i * j for i, j in zip(x0, weights[-1])]]


def dot(x, y):
    return sum(i * j for i, j in zip(x, y))


def bp(layer_ct, targets, x_nodes, weights, act_func, alpha):
    e_nodes = [[t - j for t, j in zip(targets, x_nodes[-1])]]
    e_weights = [[x * e for x, e in zip(x_nodes[-2], e_nodes[0])]]
    e_nodes.append([en * ew * activ_der(act_func, x) for en, ew, x in zip(e_nodes[0], weights[-1], x_nodes[-2])])
    for idx, wi in enumerate(weights[:-1][::-1]):
        sl = []
        for e in e_nodes[idx + 1]:
            for x in x_nodes[-idx - 3]:
                sl.append(x * e)
        e_weights.append(sl)
        e_nodes.append(
            [dot(wi[idx2::layer_ct[-idx - 3]], e_nodes[-1]) * activ_der(act_func, x)
             for idx2, x in enumerate(x_nodes[-idx - 3])])
    return [[ew * alpha + w for ew, w in zip(ew_l, w_l)] for ew_l, w_l in zip(e_weights[::-1], weights)]


def new_weights(err, layer_ct, inputs, targets, act_func, cutoff):
    weights = []
    while err > cutoff:
        weights = [[random.uniform(-2.0, 2.0) for _ in range(layer_ct[i] * layer_ct[i + 1])] for i in
                   range(len(layer_ct) - 2)] + [[random.uniform(-2.0, 2.0) for _ in range(layer_ct[-1])]]
        err = calc_error(inputs, targets, weights, layer_ct, act_func)
    return err, weights


def add_data(inputs, rad, bias, equality, targets, edge_flag):
    if edge_flag:
        x = random.uniform(-1.5, 1.5)
        if bool(random.getrandbits(1)):
            y = math.sqrt(abs(rad - x ** 2))
        else:
            y = -math.sqrt(abs(rad - x ** 2))
        y = random.uniform(y - .2, y + .2)
        inputs.append([x, y])
    else:
        inputs.append([random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5), bias])
    if equality == '<':
        if inputs[-1][0] ** 2 + inputs[-1][1] ** 2 < rad:
            targets.append([1])
        else:
            targets.append([0])
    else:
        if inputs[-1][0] ** 2 + inputs[-1][1] ** 2 > rad:
            targets.append([1])
        else:
            targets.append([0])


def calc_error(inputs, targets, weights, layer_ct, act_func):
    err = 0
    for inp, target in zip(inputs, targets):
        nodes = ff(inp.copy(), weights, act_func)
        err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2
    return err


def main():
    t_end = time.time() + 99
    st = args[0]
    st = st.replace('=', '')
    equality = st[7]
    rad = float(st[8:])
    inputs, targets = [], []
    bias = 1
    act_func = 'T3'
    layer_ct = [3, 10, 4, 1, 1]
    for i in range(100):
        add_data(inputs, rad, bias, equality, targets, False)
    err, weights = new_weights(1000, layer_ct, inputs, targets, act_func, 12)
    alpha = math.sqrt(err)
    prev_err = err
    # print(err)
    edge_flag = False
    i = 0
    while time.time() < t_end:
        if i % 1000 == 0:
            err = calc_error(inputs, targets, weights, layer_ct, act_func)
            # if err < .1:
            #     edge_flag = True
            # else:
            #     edge_flag = False
            # print(prev_err, err, prev_err - err)
            # if err > 12:
            # print(prev_err - err, prev_err, err)
            # print(err)
            # if err < .01:
            #     break
            # prev_err - err < 0 or
            if err > 12:
                err, weights = new_weights(1000, layer_ct, inputs, targets, act_func, 12)
            alpha = math.sqrt(err) if err >= 1 else err ** 2
            # prev_err = err
        add_data(inputs, rad, bias, equality, targets, edge_flag)
        inputs, targets = inputs[1:], targets[1:]
        inp, target = inputs[-1], targets[-1]
        nodes = ff(inp.copy(), weights, act_func)
        weights = bp(layer_ct, target, nodes, weights, act_func, alpha)
        # if i % 100:
        #     print(calc_error(inputs, targets, weights, layer_ct, act_func))
        i += 1
    print('Layer Counts:', *layer_ct)
    print('Weights:')
    for w in weights:
        print(*w)
    print('Error:', calc_error(inputs, targets, weights, layer_ct, act_func))


if __name__ == '__main__':
    main()
# Sai Vaka, Period 5, 2023
