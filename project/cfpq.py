from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix

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


def reachability_for_nodes_hellings(graph, cfg, start_nodes, final_nodes, nt_symbols):
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


def algorithm_matrix_based(matrices, var_productions):
    while True:
        unchanged_matrices = {var: mtrx.copy() for var, mtrx in matrices.items()}
        for first_elm, second_elm, head in var_productions:
            matrices[head] += matrices[first_elm] @ matrices[second_elm]
        if all(
            (matrices[var] - unchanged_matrices[var]).nnz == 0
            for var in matrices.keys()
        ):
            break

    triples_set = set()
    for variable, mtrx in matrices.items():
        for u, v in zip(*mtrx.nonzero()):
            triples_set.add((u, variable, v))
    return triples_set


def matrix_based(graph, cfg):
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
    nodes_num = graph.number_of_nodes()
    matrices = {
        v.value: dok_matrix((nodes_num, nodes_num), dtype=bool)
        for v in weak_cnf.variables
    }

    for v in range(nodes_num):
        for h in eps_prod_heads:
            matrices[h][v, v] = True
    for u, v, edge_data in graph.edges(data=True):
        for body, head in single_productions:
            if body == edge_data["label"]:
                matrices[head][u, v] = True
    result = algorithm_matrix_based(matrices, double_productions)
    return result


def reachability_for_nodes_matrix(graph, cfg, start_nodes, final_nodes, nt_symbols):
    result = {start_node: set() for start_node in start_nodes}
    mtrx = matrix_based(graph, cfg)
    for start_node, nt, final_node in mtrx:
        if nt == nt_symbols and start_node in start_nodes and final_node in final_nodes:
            result[start_node].add(final_node)
    return result


def from_text_matrix(graph, cfg):
    return matrix_based(graph, CFG.from_text(cfg))


def from_file_matrix(graph, filename):
    with open(filename) as file:
        return from_text_matrix(graph, file.read())
