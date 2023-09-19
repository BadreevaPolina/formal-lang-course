from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from pyformlang.regular_expression import Regex


def dfa_minimal(regular_expr):
    regex = Regex(regular_expr)
    dfa = regex.to_epsilon_nfa().to_deterministic()
    return dfa.minimize()


def graph_to_nfa(graph, start=None, final=None):
    nfa = NondeterministicFiniteAutomaton()
    start_nodes = graph.nodes if start is None else start
    final_nodes = graph.nodes if final is None else final

    for node in start_nodes:
        nfa.add_start_state(node)

    for node in final_nodes:
        nfa.add_final_state(node)

    for start, final, data in graph.edges(data=True):
        nfa.add_transition(State(start), Symbol(data["label"]), State(final))
    return nfa
