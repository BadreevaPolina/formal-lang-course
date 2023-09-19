from cfpq_data import download, graph_from_csv, labeled_two_cycles_graph

from project.finite_automata import graph_to_nfa, dfa_minimal


def test_dfa_minimal():
    dfa = dfa_minimal("abc|d")
    assert dfa.accepts(["abc"])


def test_graph_download_to_nfa_without():
    file = download("generations")
    graph_csv = graph_from_csv(file)
    nfa = graph_to_nfa(graph_csv)
    assert nfa.accepts(["onProperty"])


def test_graph_download_to_nfa_with():
    file = download("generations")
    graph_csv = graph_from_csv(file)
    nfa = graph_to_nfa(graph_csv, [65, 33], [97])
    assert not nfa.accepts(["onProperty"])


def test_graph_generate_to_nfa_without():
    graph = labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    nfa = graph_to_nfa(graph)
    assert nfa.accepts(["b"])
    assert nfa.accepts(["a", "a"])
    assert nfa.accepts(["a", "b"])


def test_graph_generate_to_nfa_with():
    graph = labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    nfa = graph_to_nfa(graph, [0], [2])
    assert not nfa.accepts(["b"])
    assert nfa.accepts(["a", "a"])
    assert not nfa.accepts(["a", "b"])


def test_graph_generate_to_nfa_with_2():
    graph = labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    nfa = graph_to_nfa(graph, [0, 2, 3], [0, 2, 3])
    assert nfa.accepts(["b"])
    assert nfa.accepts(["a", "a"])
    assert nfa.accepts(["a", "b"])
