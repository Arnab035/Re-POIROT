

def number_of_compromise_points(flow, filename):
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

    
   
