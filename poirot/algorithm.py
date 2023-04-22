# contains code from the 4 steps of the main algorithm 

from utils import *


def find_candidate_node_alignments(q_nodes_with_type, filename):
    '''
    given a set of nodes from the query graph (G_q),
    find a candidate set of nodes in the actual
    provenance graph (G_p).

    params: q_nodes_with_type -> list of (node_id, node_type) 
                        from the query graph.
            filename -> file representing provenance
                        graph.
    returns: a dictionary like:
            {node_id : [node_alignments] where
            node_id is the node from query graph
            node_alignments is the list of nodes from filename 
            that are aligned to nodes in q_nodes_with_type

    note: alignments happen based only on the type of node.
     streamspot dataset only has information about type of node.
    '''
    candidate_node_alignments = {}
    all_nodes_with_type = get_all_nodes_with_type_in_graph(filename)
    for node in q_nodes_with_type:
        for node_with_type in all_nodes_with_type:
            if node[1] == node_with_type[1]:
                if node[0] not in candidate_node_alignments:
                    candidate_node_alignments[node[0]] = [node_with_type[0]]
                else:
                    candidate_node_alignments[node[0]].append(node_with_type[0])
    return candidate_node_alignments


def select_seed_nodes(g_q_nodes_with_type, index, filename):
    '''
    params: g_q_nodes_with_type -> list of (node_id, node_type)
                          from the query graph.
            filename -> file representing provenance graph.
            index -> the indexth lowest node alignment
                     (we start with 0)
    returns: a seed node in G_q from which graph exploration
             should start.
    '''
    candidate_alignments = 
        find_candidate_node_alignments(g_q_nodes_with_type, filename)
    sorted_node_alignments = sorted(candidate_alignments, 
            key=lambda k: len(candidate_alignments[k]))
    return sorted_node_alignments[index]
    

