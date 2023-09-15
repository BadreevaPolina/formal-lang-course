from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from pyformlang.regular_expression import Regex


def dfa_minimal(regular_expr):
    regex = Regex(regular_expr)
    dfa = regex.to_epsilon_nfa().to_deterministic()
    return dfa.minimize()


def graph_to_nfa(graph, start=None, final=None):
    nfa = NondeterministicFiniteAutomaton()
    if start is None:
        for node in graph.nodes:
            nfa.add_start_state(node)
    else:
        nfa.add_start_state(start)
    if final is None:
        for node in graph.nodes:
            nfa.add_final_state(node)
    else:
        nfa.add_final_state(final)

    for start, final, data in graph.edges(data=True):
        nfa.add_transition(State(start), Symbol(data["label"]), State(final))
    return nfa
