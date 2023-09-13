import os

import pydot
from cfpq_data import labeled_two_cycles_graph

from project.graph import graph_information, two_cycles_graph


def test_graph_information_generations():
    count_edges, count_nodes, labels = graph_information("generations")
    labels_generation = {
        "range",
        "intersectionOf",
        "hasChild",
        "inverseOf",
        "hasSex",
        "sameAs",
        "type",
        "first",
        "hasSibling",
        "versionInfo",
        "someValuesFrom",
        "hasValue",
        "equivalentClass",
        "hasParent",
        "rest",
        "onProperty",
        "oneOf",
    }
    assert count_edges == 273
    assert count_nodes == 129
    assert labels == labels_generation


def test_graph_information_eclass():
    count_edges, count_nodes, labels = graph_information("eclass")
    labels_eclass = {
        "domain",
        "hierarchyCode",
        "subPropertyOf",
        "creator",
        "imports",
        "subClassOf",
        "type",
        "comment",
        "range",
        "label",
    }
    assert count_edges == 360248
    assert count_nodes == 239111
    assert labels == labels_eclass


def test_two_cycles_graph():
    file = "test.dot"
    two_cycles_graph(2, 1, ("a", "b"), file)
    (graph_from_file,) = pydot.graph_from_dot_file(file)

    g = labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    edges = list(g.edges(data=True))
    graph = pydot.Dot()
    for edge in edges:
        pydot_edge = pydot.Edge(edge[0], edge[1], label=edge[2]["label"])
        graph.add_edge(pydot_edge)

    assert str(graph) == str(graph_from_file)
    os.remove("test.dot")
