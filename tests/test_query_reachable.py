from cfpq_data import labeled_two_cycles_graph
from networkx import MultiDiGraph

from project.query_reachable import query_reachable_states


def test_query_reachable_states_1():
    regex = "a|c"
    graph = MultiDiGraph()
    nodes = [0, 1, 2, 3]
    edges = [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    assert query_reachable_states(graph, [0], [1, 2, 3], regex, True) == [{1}]
    assert query_reachable_states(graph, [0, 2], [1, 2, 3], regex, True) == [
        {1},
        {2, 3},
    ]
    assert query_reachable_states(graph, [0, 2], [1, 2, 3], regex, False) == {1, 2, 3}


def test_query_reachable_states_2():
    regex = "ab|a"
    graph = MultiDiGraph()
    nodes = [0, 1, 2, 3]
    edges = [
        (0, 1, {"label": "a"}),
        (1, 2, {"label": "b"}),
        (2, 3, {"label": "c"}),
        (0, 2, {"label": "b"}),
    ]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    assert query_reachable_states(graph, [0], [1], regex, False) == {1}


def test_query_reachable_states_3():
    regex = "(a*|b)"
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    assert query_reachable_states(graph, [0, 2], [1, 2, 3], regex, True) == [
        {1, 2, 3},
        {1, 2, 3},
    ]


def test_query_reachable_states_4():
    regex = "(a*|b)"
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    assert query_reachable_states(graph, [0, 2], [1, 2, 3], regex, False) == {1, 2, 3}


def test_query_reachable_states_5():
    regex = "(a|b)(aa)*"
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    assert query_reachable_states(graph, [0, 1, 2, 3], [0], regex, True) == [
        {0},
        {0},
        {0},
        {0},
    ]
    assert query_reachable_states(graph, [0, 1, 2, 3], [0], regex, False) == {0}
