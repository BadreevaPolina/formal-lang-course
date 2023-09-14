import pydot
from cfpq_data import *


def graph_information(name_graph):
    path = download(name_graph)
    graph = graph_from_csv(path)
    count_edges = len(list(graph.edges(data=True)))
    count_nodes = graph.number_of_nodes()
    labels = set(get_sorted_labels(graph))
    return count_edges, count_nodes, labels


def two_cycles_graph(n, m, labels, path):
    g = labeled_two_cycles_graph(n, m, labels=labels)
    edges = list(g.edges(data=True))
    graph = pydot.Dot()
    for edge in edges:
        pydot_edge = pydot.Edge(edge[0], edge[1], label=edge[2]["label"])
        graph.add_edge(pydot_edge)
    with open(path, "w") as file:
        file.write(graph.to_string().replace("\n", ""))
