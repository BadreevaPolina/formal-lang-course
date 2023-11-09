import os

from cfpq_data import labeled_two_cycles_graph
from pyformlang.cfg import CFG, Variable

from project.hellings import (
    from_text_hellings,
    from_file_hellings,
    reachability_for_nodes,
)


def test_reachability_for_nodes_1():
    cfg = "S -> A B\nS -> epsilon\nS1 -> S B\nA -> a\nS -> S1\nB -> b"
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))
    expected = {0: {4}, 2: {2}}
    assert (
        reachability_for_nodes(graph, CFG.from_text(cfg), [0, 2], [2, 4], Variable("S"))
        == expected
    )


def test_reachability_for_nodes_2():
    cfg = "S -> A B | C\nC -> A\nA -> a\nB -> b\n"
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))
    expected = {1: {2}, 2: {3}}
    assert (
        reachability_for_nodes(graph, CFG.from_text(cfg), [1, 2], [2, 3], Variable("S"))
        == expected
    )


def test_reachability_for_nodes_3():
    cfg = "S -> A | b\nA -> a\n"
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))
    expected = {0: {4}, 1: {2}, 2: {3}}
    assert (
        reachability_for_nodes(
            graph, CFG.from_text(cfg), [0, 1, 2], [2, 3, 4], Variable("S")
        )
        == expected
    )


def test_from_text_hellings_1():
    cfg = "S -> A | b\nA -> a\n"
    graph = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    expected = {(0, "S", 1), (0, "S", 2), (1, "S", 0), (2, "S", 0)}
    assert from_text_hellings(graph, cfg) == expected


def test_from_file_hellings_1():
    filename = "cfg.txt"
    cfg = "S -> A | b\nA -> a\n"
    graph = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    with open(filename, "w") as f:
        f.write(cfg)
    expected = {(0, "S", 1), (0, "S", 2), (1, "S", 0), (2, "S", 0)}
    actual = from_file_hellings(graph, filename)
    os.remove(filename)
    assert actual == expected
