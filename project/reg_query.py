from scipy.sparse import kron, dok_matrix

from project.finite_automata import dfa_minimal, graph_to_nfa


def intersect_automata(automaton1, automaton2):
    matrix = {}
    automaton1_matrix = automaton_to_matrix(automaton1)
    automaton2_matrix = automaton_to_matrix(automaton2)
    labels = automaton1_matrix.keys() & automaton2_matrix.keys()
    for label in labels:
        matrix[label] = kron(automaton1_matrix[label], automaton2_matrix[label])
    return matrix


def automaton_to_matrix(automaton):
    matrix = {}
    states = automaton.states
    state_indices = {state: index for index, state in enumerate(states)}

    for first_state, transition in automaton.to_dict().items():
        for label, second_states in transition.items():
            second_states = (
                second_states if isinstance(second_states, set) else {second_states}
            )
            for state in second_states:
                if label not in matrix:
                    matrix[label] = dok_matrix((len(states), len(states)), dtype=int)
                first_state_index = state_indices.get(first_state)
                second_state_index = state_indices.get(state)
                matrix[label][first_state_index, second_state_index] = 1
    return matrix


def execute_regex_query(graph, start_nodes, final_nodes, regex):
    dfa_regex = dfa_minimal(regex)
    nfa_graph = graph_to_nfa(graph, start_nodes, final_nodes)
    start_states, final_states = find_start_and_final_states(nfa_graph, dfa_regex)

    result_matrix = intersect_automata(nfa_graph, dfa_regex)
    transitive = get_transitive_closure(result_matrix)

    result = set()
    for first_state, second_state in transitive:
        if first_state in start_states and second_state in final_states:
            result.add(
                (
                    first_state // len(dfa_regex.states),
                    second_state // len(dfa_regex.states),
                )
            )
    return result


def find_start_and_final_states(automaton1, automaton2):
    start_states, final_states = set(), set()
    state1_indices = {state: index for index, state in enumerate(automaton1.states)}
    state2_indices = {state: index for index, state in enumerate(automaton2.states)}

    for state1, index1 in state1_indices.items():
        for state2, index2 in state2_indices.items():
            state_index = index1 * len(automaton2.states) + index2
            if state1 in automaton1.start_states and state2 in automaton2.start_states:
                start_states.add(state_index)
            if state1 in automaton1.final_states and state2 in automaton2.final_states:
                final_states.add(state_index)
    return start_states, final_states


def get_transitive_closure(matrix):
    if len(matrix) == 0:
        return dok_matrix((0, 0), dtype=int)

    transitive_closure = sum(matrix.values())
    prev = transitive_closure.count_nonzero()
    curr = 0
    while prev != curr:
        transitive_closure += transitive_closure @ transitive_closure
        prev = curr
        curr = transitive_closure.count_nonzero()
    return zip(*transitive_closure.nonzero())
