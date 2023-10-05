from enum import Enum

from scipy.sparse import dok_matrix, block_diag, identity, hstack
from project.finite_automata import dfa_minimal, graph_to_nfa


class ReachabilityOptions(Enum):
    NOT_SEPARATE = False
    SEPARATE = True


def automaton_to_matrix(automaton):
    state_to_index = {state: index for index, state in enumerate(automaton.states)}
    num_states = len(automaton.states)
    matrix = {}

    for first_state, symbol, second_state in automaton:
        matrix.setdefault(symbol, dok_matrix((num_states, num_states), dtype=int))
        matrix[symbol][state_to_index[first_state], state_to_index[second_state]] = 1

    start_indices = [state_to_index[state] for state in automaton.start_states]
    all_indices = [state_to_index[state] for state in automaton.states]
    return matrix, start_indices, all_indices


def find_reachable_states(graph, start_states, regex):
    reachable_states = []

    for start_state in start_states:
        dfa_regex = dfa_minimal(regex)
        nfa_graph = graph_to_nfa(graph, start_state)

        dfa_matrix, dfa_start_indices, dfa_all_indices = automaton_to_matrix(dfa_regex)
        nfa_matrix, nfa_start_indices, nfa_all_indices = automaton_to_matrix(nfa_graph)
        nfa_start_indices = [len(dfa_all_indices) + i for i in nfa_start_indices]
        combined_matrices = combine_transition_matrices(dfa_matrix, nfa_matrix)

        num_states_dfa = len(dfa_all_indices)
        num_combined_states = len(dfa_all_indices) + len(nfa_all_indices)

        reachable = initialize_reachable_matrix(
            num_states_dfa, num_combined_states, dfa_start_indices, nfa_start_indices
        )
        current = reachable
        zeros = None

        while zeros is None or reachable.count_nonzero() != zeros:
            successor = calculate_successor_matrix(
                num_states_dfa,
                num_combined_states,
                combined_matrices,
                current,
                dfa_all_indices,
            )
            zeros = reachable.count_nonzero()
            reachable += successor
            current = successor

        final_states = find_final_states(
            reachable, dfa_all_indices, nfa_all_indices, nfa_graph.states
        )
        reachable_states.append(final_states)
    return reachable_states


def combine_transition_matrices(automaton1, automaton2):
    matrix = {}
    labels = automaton1.keys() & automaton2.keys()
    for label in labels:
        matrix[label] = block_diag((automaton1[label], automaton2[label]))
    return matrix


def initialize_reachable_matrix(
    num_states_dfa, num_combined_states, dfa_start_indices, nfa_start_indices
):
    reachable_matrix = hstack(
        [
            identity(num_states_dfa, dtype=int, format="dok"),
            dok_matrix(
                (num_states_dfa, num_combined_states - num_states_dfa), dtype=int
            ),
        ],
        format="dok",
    )
    for x in dfa_start_indices:
        for y in nfa_start_indices:
            reachable_matrix[x, y] = 1
    return reachable_matrix


def calculate_successor_matrix(
    num_states_dfa, num_combined_states, combined_matrices, current, dfa_all_indices
):
    identity_matrix = identity(num_states_dfa, dtype=int)
    zero_matrix = dok_matrix(
        (num_states_dfa, num_combined_states - num_states_dfa), dtype=int
    )
    successor_matrix = hstack([identity_matrix, zero_matrix], format="dok")
    for matrix in combined_matrices.values():
        new_reachable = current @ matrix
        for i, j in zip(range(len(dfa_all_indices)), range(len(dfa_all_indices))):
            successor_matrix[j, len(dfa_all_indices) :] += new_reachable[
                i, len(dfa_all_indices) :
            ]
    return successor_matrix


def find_final_states(reachable_matrix, dfa_all_indices, nfa_all_indices, nfa_states):
    nfa_states_list = list(nfa_states)
    final_states = set()
    for i in dfa_all_indices:
        for j in nfa_all_indices:
            if reachable_matrix[i, len(dfa_all_indices) + j]:
                final_states.add(nfa_states_list[j])
    return final_states


def query_reachable_states(
    graph, start, final, regex, option=ReachabilityOptions.SEPARATE
):
    start_states = (
        [[s] for s in start] if option == ReachabilityOptions.SEPARATE else [start]
    )
    reachable_states = find_reachable_states(graph, start_states, regex)
    filtered_states = filter_reachable_states(reachable_states, final)
    result = (
        filtered_states
        if option == ReachabilityOptions.SEPARATE
        else filtered_states[0]
    )
    return result


def filter_reachable_states(reachable_states, final):
    result = []
    for state_set in reachable_states:
        filtered_state_set = {j for j in state_set if j in final}
        result.append(filtered_state_set)
    return result
