from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(self, start_symbol=None, productions=None):
        self.start_symbol = start_symbol
        self.productions = productions

    def ecfg_from_text(self, text, start_symbol=Variable("S")):
        productions = {}
        for t in text.splitlines():
            line = t.strip().split("->")
            if len(line) == 2:
                head_t, body_t = line[0], line[1]
                head = Variable(head_t.strip())
                body = Regex(body_t.strip())
                productions[head] = body
        self.productions = productions
        self.start_symbol = start_symbol
        return self

    def ecfg_from_file(self, filename):
        with open(filename) as file:
            cfg_str = file.read()
            return self.ecfg_from_text(cfg_str)

    def ecfg_from_cfg(self, cnf, start_symbol=Variable("S")):
        prod = {}
        for p in cnf.productions:
            body = Regex(
                " ".join(symbol.value for symbol in p.body) if len(p.body) > 0 else ""
            )
            prod[p.head] = prod[p.head].union(body) if p.head in prod else body
        self.productions = prod
        self.start_symbol = start_symbol
        return self
