from cfpq_data import labeled_two_cycles_graph
from pyformlang.finite_automaton import State, NondeterministicFiniteAutomaton, Symbol

from project.finite_automata import graph_to_nfa, dfa_minimal
from project.reg_query import execute_regex_query, intersect_automata


def test_intersect_automata_1():
    graph = labeled_two_cycles_graph(1, 1, labels=("a", "b"))
    dfa_regex = dfa_minimal("b")
    nfa_graph = graph_to_nfa(graph, [0], [3])
    matrix = intersect_automata(nfa_graph, dfa_regex)
    answer = []
    for m in matrix:
        row_indices, col_indices = matrix[m].nonzero()
        for row, col in zip(row_indices, col_indices):
            answer.append([row, col])
    assert answer == [[1, 4], [5, 0]] or answer == [[0, 5], [4, 1]]


def test_intersect_automata_2():
    states = [State(0), State(1), State(2), State(3)]
    nfa_graph = NondeterministicFiniteAutomaton()
    nfa_graph.add_start_state(states[2])
    nfa_graph.add_start_state(states[3])
    nfa_graph.add_final_state(states[0])
    nfa_graph.add_final_state(states[1])
    nfa_graph.add_transitions(
        [
            (states[0], Symbol("a"), states[2]),
            (states[1], Symbol("a"), states[0]),
            (states[3], Symbol("a"), states[0]),
            (states[0], Symbol("b"), states[0]),
            (states[2], Symbol("b"), states[2]),
        ]
    )
    dfa_regex = dfa_minimal("b")
    matrix = intersect_automata(nfa_graph, dfa_regex)
    answer = []
    for m in matrix:
        row_indices, col_indices = matrix[m].nonzero()
        for row, col in zip(row_indices, col_indices):
            answer.append([row, col])

    assert answer == [[0, 1], [4, 5]] or answer == [[1, 0], [5, 4]]


def test_regular_path_query_1():
    graph_ex = labeled_two_cycles_graph(2, 2, labels=("a", "b"))
    result = execute_regex_query(graph_ex, [0, 1], [2, 3], "(a + b)* b (a + b)*")
    assert result == {(1, 2), (0, 2), (0, 3), (1, 3)}


def test_regular_path_query_2():
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    result = execute_regex_query(graph, [0], [1], "(a|b)(aa)*")
    assert result == {(0, 1)}


def test_regular_path_query_3():
    graph = labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    result = execute_regex_query(graph, [0, 1, 2, 3], [0, 1, 2, 3], "a* b b*")
    assert result == {(0, 0), (0, 3), (2, 0), (3, 0), (2, 3), (3, 3), (1, 0), (1, 3)}
