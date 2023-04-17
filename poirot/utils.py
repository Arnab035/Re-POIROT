
process_nodes = []

def get_all_nodes_in_graph(filename):
    '''
    most of the datasets have nodes not numbered
    sequentially, so we need to call this function
    this returns a list of all unique nodes in the graph
    from the edge list
    params: filename containing the graph
    returns: a list containing the node numbers
    '''
    unique_nodes = set()
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            unique_nodes.add(entry[0])
            unique_nodes.add(entry[1])
    return list(unique_nodes)

def get_all_edges_in_graph(filename):
    '''
    this utility function returns the edges in
    the graph as a list of lists
    params: filename
    returns: a list containing the edges.
             something like this:
             [[2, 3], [4, 5], [6, 7]}
    '''
    edges = []
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            edges.append([entry[0], entry[1]])
    return edges


def find_ancestors(filename):
    '''
    finds ancestors of all the vertices in graph
    params: filename
    returns: a dict containing ancestors of all vertices
             e.g. for edges [[0,2],[1,2],[2,3],[3,4],[2,5]]
     the answer is: {0: [], 1: [], 2: [0, 1], 3: [0, 1, 2], 
                   4: [0, 1, 2, 3], 5: [0, 1, 2]}
    '''
    graph = {}
    nodes = get_all_nodes_in_graph(filename)
    edges = get_all_edges_in_graph(filename)
    for a, b in edges:
        graph[b] = graph.get(b, []) + [a]

    op = {i: [] for i in nodes}
    for a in graph:
        visited = set()
        paths = [a]
        while len(paths) > 0:
            curr = paths.pop()
            for b in graph.get(curr, []):
                if b not in visited:
                    visited.add(b)
                    paths.append(b)
            op[a] = sorted(visited)
    return op

def find_common_ancestors(process_nodes, ancestors):
    '''
    finds common ancestors of a bunch of process nodes
    params: process_nodes: list of process nodes,
                           possibly from a flow
            ancestors: a dict containing ancestors of all
                       vertices
    returns: a list containing common ancestors of the
             process nodes
    '''
    ancestors_of_nodes = []
    for process_node in process_nodes:
        ancestors_of_nodes.append(ancestors[process_node])
    result = set(ancestors_of_nodes[0])
    for s in ancestors_of_nodes[1:]:
        result.intersection_update(s)
    return result
   
def find_unique_nodes_from_flow(flow):
    '''
    given a flow, this function finds unique nodes
    in the flow
    params: flow(a flow is represented by a list of edges)
    returns: a list containing the unique nodes in the flow
    '''
    unique_nodes_in_flow = []
    for edge in flow:
        unique_nodes_in_flow.append(edge[0])
        unique_nodes_in_flow.append(edge[1])
    return list(set(unique_nodes_in_flow))

def create_list_of_process_nodes(filename)
    '''
    given a provenance graph, generate a list of all the 
    process nodes in the graph
    param(s): filename representing the provenance graph
    populates global variable called process_nodes
    '''
    global process_nodes
    with open(filename, 'r') as f:
        for line in f:
            entry = line.split()
            if (entry[2].split(':')[0] == 'a'):
                process_nodes.append(entry[0])
            elif (entry[2].split(':')[1] == 'a'):
                process_nodes.append(entry[1])

def check_if_node_is_process_node(node)
    '''b
    given a node represented as an integer,
    report if it is a process node
    param(s): node, represented as an integer
    returns: bool, true if process node, false if not
    '''
    if node in process_nodes:
        return True
    else:
        return False
