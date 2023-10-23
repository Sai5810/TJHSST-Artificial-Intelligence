import math
import random
import csv
import sys


def dot(x, y):
    return sum(i * j for i, j in zip(x, y))


class NN:
    def __init__(self, layer_ct, cutoff, inputs, targets, alpha, weight_range=2, bias=1, afc='T3'):
        self.weights = None
        self.bias = bias
        self.afc = afc
        self.layer_ct = layer_ct
        self.cutoff = cutoff
        self.weight_range = weight_range
        self.inputs = inputs
        self.targets = targets
        self.err = math.inf
        self.alpha = alpha

    def ff(self, x0):
        nodes = [x0]
        for wl in self.weights[:-1]:
            nex = []
            tot = 0
            idx = 0
            for w in wl:
                tot += w * x0[idx]
                idx += 1
                if idx >= len(x0):
                    idx = 0
                    nex.append(self.activate(tot))
                    tot = 0
            nodes.append(nex)
            x0 = nex
        return nodes + [[i * j for i, j in zip(x0, self.weights[-1])]]

    def calc_error(self):
        self.err = 0
        for inp, target in zip(self.inputs, self.targets):
            nodes = self.ff(inp.copy())
            self.err += sum((t - n) ** 2 for t, n in zip(target, nodes[-1])) / 2

    def create_weights(self):
        while self.err > self.cutoff:
            self.weights = [[random.uniform(-self.weight_range, self.weight_range) for _ in
                             range(self.layer_ct[i] * self.layer_ct[i + 1])] for i in range(len(self.layer_ct) - 2)] + [
                               [random.uniform(-self.weight_range, self.weight_range) for _ in
                                range(self.layer_ct[-1])]]
            self.calc_error()

    def activate(self, x):
        if self.afc == 'T1':
            return x
        elif self.afc == 'T2':
            return x if x > 0 else 0
        elif self.afc == 'T3':
            return 1 / (1 + math.exp(-x))
        elif self.afc == 'T4':
            return 2 / (1 + math.exp(-x)) - 1

    def activ_der(self, y):
        if self.afc == 'T1':
            return 1
        elif self.afc == 'T2':
            return 1 if y > 0 else 0
        elif self.afc == 'T3':
            return y * (1 - y)
        elif self.afc == 'T4':
            return .5 * (y + 1) * (1 - y)

    def bp(self, x_nodes, alpha):
        e_nodes = [[t - j for t, j in zip(self.targets, x_nodes[-1])]]
        e_weights = [[x * e for x, e in zip(x_nodes[-2], e_nodes[0])]]
        e_nodes.append([en * ew * self.activ_der(x) for en, ew, x in zip(e_nodes[0], self.weights[-1], x_nodes[-2])])
        for idx, wi in enumerate(self.weights[:-1][::-1]):
            sl = []
            for e in e_nodes[idx + 1]:
                for x in x_nodes[-idx - 3]:
                    sl.append(x * e)
            e_weights.append(sl)
            e_nodes.append(
                [dot(wi[idx2::self.layer_ct[-idx - 3]], e_nodes[-1]) * self.activ_der(x)
                 for idx2, x in enumerate(x_nodes[-idx - 3])])
        return [[ew * alpha + w for ew, w in zip(ew_l, w_l)] for ew_l, w_l in zip(e_weights[::-1], self.weights)]

    def run(self, epochs):
        for i in range(epochs):
            if i % 1000 == 0:
                self.calc_error()
                if self.err > 12:
                    self.create_weights()
                self.alpha = math.sqrt(self.err) if self.err >= 1 else self.err ** 2
            for inp, target in zip(self.inputs, self.targets):
                nodes = self.ff(inp.copy())
                self.weights = self.bp(target, nodes)


def main():
    inputs = []
    targets = []
    with open(sys.argv[1], newline='') as csvfile:
        for row in csv.reader(csvfile, delimiter=' ', quotechar='|'):
            row = [int(i) for i in row[0].split(',')]
            inp = [0] * 10
            inp[row[0] - 1] = 1
            inputs.append(inp)
            target = [i / 255 for i in row[1:]]
            targets.append(target)
    print(targets)
    net = NN()


if __name__ == '__main__':
    main()
