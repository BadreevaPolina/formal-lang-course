from pyformlang.cfg import CFG

from project.weak_cnf import to_weak_cnf


def algorithm_hellings(triples_set, var_productions):
    copied = triples_set.copy()
    while copied:
        i, head_n, j = copied.pop()
        step = set()

        for u, head_m, v in triples_set:
            if v == i:
                for first_elm, second_elm, head in var_productions:
                    if (
                        first_elm == head_m
                        and second_elm == head_n
                        and (u, head, j) not in triples_set
                    ):
                        step.add((u, head, j))
        triples_set.update(step)
        copied.update(step)

        step.clear()

        for u, head_m, v in triples_set:
            if u == j:
                for first_elm, second_elm, head in var_productions:
                    if (
                        first_elm == head_n
                        and second_elm == head_m
                        and (i, head, v) not in triples_set
                    ):
                        step.add((i, head, v))
        triples_set.update(step)
        copied.update(step)


def hellings(graph, cfg):
    weak_cnf = to_weak_cnf(cfg)
    eps_prod_heads = [p.head.value for p in weak_cnf.productions if not p.body]
    single_productions = {
        (p.body[0].value, p.head.value)
        for p in weak_cnf.productions
        if len(p.body) == 1
    }
    double_productions = {
        (p.body[0].value, p.body[1].value, p.head.value)
        for p in weak_cnf.productions
        if len(p.body) == 2
    }

    triples_set = {
        (v, h, v) for v in range(graph.number_of_nodes()) for h in eps_prod_heads
    }
    for u, v, edge_data in graph.edges(data=True):
        for body, head in single_productions:
            if body == edge_data["label"]:
                triples_set.add((u, head, v))

    algorithm_hellings(triples_set, double_productions)
    return triples_set


def reachability_for_nodes(graph, cfg, start_nodes, final_nodes, nt_symbols):
    result = {start_node: set() for start_node in start_nodes}
    hell = hellings(graph, cfg)
    for start_node, nt, final_node in hell:
        if nt == nt_symbols and start_node in start_nodes and final_node in final_nodes:
            result[start_node].add(final_node)
    return result


def from_text_hellings(graph, cfg):
    return hellings(graph, CFG.from_text(cfg))


def from_file_hellings(graph, filename):
    with open(filename) as file:
        return from_text_hellings(graph, file.read())
