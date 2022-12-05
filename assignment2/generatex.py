import argparse
import random
from collections import defaultdict


class Node:
    def __init__(self, symbol, terminal):
        self.next = []
        self.terminal = terminal
        self.symbol = symbol


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self._parse_tree = []
        self.tree = ""
        self.entity = None

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules


    def gen(self, symbol):
        if symbol[-1] == "*":
            if not self.entity:
                x = self.tree[:]
                self.entity = self.gen(symbol[:-1])
                self.entity_tree = self.tree[len(x):]
                symbol = self.entity
                return symbol
            else:
                self.tree += self.entity_tree
                return self.entity
        if self.is_terminal(symbol):
            self._parse_tree.append(('term', symbol))
            self.tree += " " + symbol
            return symbol
        else:
            if symbol == 'NUM':
                expansion = [str(random.randint(2, 100))]
            else:
                expansion = self.random_expansion(symbol)
            self.tree += f" ({symbol} " if symbol != 'ROOT' else f"({symbol} "
            self._parse_tree.append(('non-term', symbol))
            path = [self.gen(s) for s in expansion]
            self.tree += ')'
            return " ".join(path)

    def random_sent(self):
        self._parse_tree.clear()
        self.tree = ""
        self.entity = None
        return (self.gen("ROOT"), self.tree)

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def print_sentences(grammar, n, t=False):
    pcfg = PCFG.from_file(grammar)
    for i in range(n):
        sent, tree = pcfg.random_sent()
        print(sent)
        if t:
            print(tree)


def main():
    parser = argparse.ArgumentParser(description='flags parser')
    # Required positional argument
    parser.add_argument('grammar', type=str,
                        help='A grammar file to be used')
    # Optional argument
    parser.add_argument('-n', type=int, default=1,
                        help='number of sentences to make')
    # Switch
    parser.add_argument('-t', default=False, action='store_true',
                        help='A boolean switch')

    args = parser.parse_args()
    print_sentences(args.grammar, args.n, args.t)


if __name__ == '__main__':
    main()
