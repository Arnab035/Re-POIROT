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
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            if entry[0] in graph:
                graph[entry[0]].append(entry[1])
            else:
                graph[entry[0]] = []
    # now that we have graph, try to find all paths
    # between the two nodes node_a and node_b
    all_flows = find_all_paths(graph, node_a, node_b)

    # now that we have all paths/flows, find the minimum
    # number of compromise points for the attacker in
    # these flows/paths
    gamma = 0
    for flow in all_flows:
        cmin = min_number_of_compromise_points(flow, filename)
        if cmin <= threshold:
            gamma = max(gamma, 1/cmin)
    print("The influence score between nodes: {} and {} is {}".format(node_a, node_b,
                                   gamma))

