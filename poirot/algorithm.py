# contains code from the 4 steps of the main algorithm

from utils import *
from scores import *

# step 1
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


# step 2
def select_seed_nodes(candidate_alignments, index):
    '''
    params: g_q_nodes_with_type -> list of (node_id, node_type)
                          from the query graph.
            filename -> file representing provenance graph.
            index -> the indexth lowest node alignment
                     (we start with 0)
    returns: a seed node in G_q from which graph exploration
             should start.
    '''
    sorted_node_alignments = sorted(candidate_alignments,
            key=lambda k: len(candidate_alignments[k]))
    return sorted_node_alignments[index]

#step 3
def find_subset_of_candidate_node_alignments(g_q_nodes_with_type,
        filename):
    '''
    params: g_q_nodes_with_type -> list of (node_id, node_type)
                           from the query graph.
            filename -> filename containing
                                    provenance graph
    result: {node_id : [subset_node_alignments]} where node_id is the
            node from query graph.
            subset_node_alignments is the list of node alignments
            which are reachable from seed node alignments using a
            backward/forward search
    '''
    candidate_node_alignments = find_candidate_node_alignments(g_q_nodes_with_type,
            provenance_graph_filename)
    # finds seed node with lowest number of alignments
    seed_node = select_seed_nodes(candidate_node_alignments, 0)
    start_nodes = candidate_node_alignments[seed_node]
                      if seed_node in candidate_node_alignments else []
    # construct provenance graph
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            if int(entry[0]) in graph:
                graph[int(entry[0])].add(int(entry[1]))
            else:
                graph[int(entry[0])] = set()
    graph = {key: list(value) for key, value in graph.items()}

    # do backward traversal
    # for this we construct another provenance graph
    # where the edges are in reverse
    reverse_graph = {}
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            if int(entry[1]) in graph:
                reverse_graph[int(entry[1])].add(int(entry[0]))
            else:
                reverse_graph[int(entry[1])] = set()

    reverse_graph = {key: list(value) for key, value in reverse_graph.items()}

    # do forward and backward traversal
    #TODO: optimization using influence score.
    all_nodes_visited = set()
    for nodes in start_nodes:
        visited = set()
        do_dfs(graph, nodes, visited)
        backward_visited = set()
        do_dfs(reverse_graph, nodes, backward_visited)
        all_nodes_visited = visited.union(backward_visited)

    # in candidate_node_alignments, only keep those nodes that are found
    # in the backward and forward traversal we did.
    for node_alignment in candidate_node_alignments:
        candidate_node_alignments[node_alignment]
                  = list(set(candidate_node_alignments[node_alignment]) & all_nodes_visited)

    return candidate_node_alignments


# do step 4
def find_graph_alignment(query_graph_filename, provenance_graph_filename, threshold):
    '''
    params: query_graph_filename-> a filename representing the query graph
            provenance_graph_filename -> a filename representing the provenance graph
            threshold -> the threshold used for computing influence score
    returns: a dict {g_q : g_p} where the keys "g_q" represent the nodes of the
             query graph and values "g_p" are a subset of candidate node alignments
             found in step 2 (usually, the best node alignment),
             this represents the best graph alignment
    '''
    # maintain aligned nodes
    aligned_nodes = {}
    # find all nodes in query graph with type
    query_all_nodes_with_type =
             get_all_nodes_with_type_in_graph(query_graph_filename)

    # find candidate node alignments from step 3
    candidate_node_alignments =
             find_subset_of_candidate_node_alignments(query_all_nodes_with_type,
                                            provenance_graph_filename)

    # construct query graph
    query_graph = {}
    with open(query_graph_filename, 'r') as f:
        for line in f:
            entry = line.split()
            if int(entry[0]) in query_graph:
                query_graph[int(entry[0])].add(int(entry[1]))
            else:
                query_graph[int(entry[0])] = set()

    # construct reverse query graph
    reverse_query_graph = {}
    with open(query_graph_filename, 'r') as f:
        for line in f:
            entry = line.split()
            if int(entry[1]) in reverse_query_graph:
                reverse_query_graph[int(entry[1])].add(int(entry[0]))
            else:
                reverse_query_graph[int(entry[1])] = set()

    # now for each of the candidate nodes of query graph, try to find the
    # best alignment using the selection function
    for candidate_node in candidate_node_alignments:
        out_visited = set()
        in_visited = set()
        do_dfs(query_graph, candidate_node, out_visited)
        do_dfs(reverse_query_graph, candidate_node, in_visited)
        candidate_node_alignment_scores = {}
        for candidate_aligned_node in candidate_node_alignments[candidate_node]:
            # for all outgoing flows in query graph
            for visited_node in out_visited:
                # node in query graph is not aligned yet
                if visited_node not in aligned_nodes:
                    # find maximum influence score of candidate_node
                    # and all candidate nodes of this visited_node
                    influence_scores = []
                    for candidate_visited_node in candidate_node_alignments[visited_node]:
                        influence_score = compute_influence_score(candidate_node,
                                       candidate_visited_node, threshold,
                                       provenance_graph_filename)
                        influence_scores.append(influence_score)
                    out_final_influence_score = max(influence_scores)
                # node in query graph is aligned
                else:
                    out_final_influence_score = compute_influence_score(candidate_node,
                                      aligned_nodes[visited_node], threshold,
                                      provenance_graph_filename)
            # do the same for all incoming flows in query graph
            for visited_node in in_visited:
                # node in query graph is not aligned yet
                if visited_node not in aligned_nodes:
                    # find max. influence score of candidate_node
                    # and all candidate nodes of this visited_node
                    influence_scores = []
                    for candidate_visited_node in candidate_node_alignments[visited_node]:
                        influence_score = compute_influence_score(candidate_node,
                                       candidate_visited_node, threshold,
                                       provenance_graph_filename)
                        influence_scores.append(influence_score)
                    in_final_influence_score = max(influence_scores)
                # node in query graph is aligned
                else:
                    in_final_influence_score = compute_influence_score(candidate_node,
                                     aligned_nodes[visited_node], threshold,
                                     provenance_graph_filename)
            total_influence_score = out_final_influence_score +
                                     in_final_influence_score
            candidate_node_alignment_scores[candidate_aligned_node] = total_influence_score
        aligned_nodes[candidate_node] = max(candidate_node_alignment_scores,
                                            key=candidate_node_alignment_scores.get)
    return aligned_nodes
