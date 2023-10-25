from pyformlang.cfg import CFG


def to_weak_cnf(cfg):
    weak_cnf = cfg.eliminate_unit_productions().remove_useless_symbols()
    start_symbol = weak_cnf._start_symbol
    productions = weak_cnf._decompose_productions(
        weak_cnf._get_productions_with_only_single_terminals()
    )
    return CFG(start_symbol=start_symbol, productions=set(productions))


def weak_cnf_from_file(filename):
    with open(filename) as src:
        initial_cfg = CFG.from_text(src.read())
    return to_weak_cnf(initial_cfg)
