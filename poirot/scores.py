from utils import *

# in this project,
# a flow is represented by a list of nodes
# for e.g. a flow between two nodes 1 & 4 can be
# represented as: [1, 2, 3, 4] i.e. 1->2->3->4

# this computes C_min(i-->j) in the influence score
def min_number_of_compromise_points(flow, filename):
    '''
    Given a flow of nodes, compute
    the number of compromise points for the
    attacker
    params: flow: a path starting at node i and
                  ending at node j
            filename: filename containing graph
    '''
    # note, for a flow, C_min (i-->j) if i is a
    # parent process and j is a child process,
    # then C_min(i-->j) == 1.
    if len(flow) == 2:
        if check_if_child_process(flow[0], flow[1], filename):
            return 1
    process_nodes = []
    unique_nodes = find_unique_nodes_from_flow(flow)
    for unique_node in unique_nodes:
        if check_if_node_is_process_node(unique_node):
            process_nodes.append(unique_node)

    # find common ancestors of process nodes.
    ancestors = find_ancestors(filename)
    common_ancestors = find_common_ancestors(process_nodes, ancestors)
    # as per the paper, the number of compromise points for the attacker
    # is the number of unique, common ancestors for process nodes in the
    # flow
    return len(common_ancestors)


def compute_influence_score(node_a, node_b, threshold, filename):
    '''
    This computes the influence score gamma(i, j) (page 1800)
    where i and j are the two nodes between whom the
    influence score is computed.
    params: start node: node_a
          : end node: node_b
          : threshold: a threshold value C_thr
          : filename: the filename representing the graph
    returns: the influence score, gamma(i, j)
    '''
    graph = construct_graph(filename)
    # now that we have graph, try to find all paths
    # between the two nodes node_a and node_b
    all_flows = find_all_paths(graph, node_a, node_b)
    # now that we have all paths/flows, find the minimum
    # number of compromise points for the attacker in
    # these flows/paths
    gamma = 0
    for flow in all_flows:
        cmin = min_number_of_compromise_points(flow, filename)
        if cmin != 0 and cmin <= threshold:
            gamma = max(gamma, 1/cmin)
    print("The influence score between nodes: {} and {} is {}".format(node_a, node_b,
                                   gamma))
    return gamma

def compute_alignment_score(query_graph_filename, provenance_graph_filename,
                                    aligned_nodes):
    '''
    This computes the alignment score between two graph alignments
    S(Gq :: Gp) where Gq is query graph and Gp is alignment from
    provenance graph

    params: query_graph_filename
            provenance_graph_filename
            aligned_nodes obtained from step 4 of poirot
    returns: alignment score as outlined in equation 2.
    '''
    query_graph = construct_graph(query_graph_filename)
    # find all flows in query graph, do dfs
    # over all nodes
    all_nodes = get_all_nodes_in_graph(query_graph_filename)
    total_influence_score = 0
    for node in all_nodes:
        visited = set()
        do_dfs(query_graph, node, visited)
        for visited_node in visited:
            influence_score = compute_influence_score(aligned_nodes[node],
                    aligned_nodes[visited_node], threshold,
                    provenance_graph_filename)
            total_influence_score += influence_score
            num_flows += 1
    return total_influence_score/num_flows
