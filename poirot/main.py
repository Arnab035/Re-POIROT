import sys
from scores import *
from algorithm import *
from utils import *

if __name__ == "__main__":
    print("Starting Poirot...")
    if len(sys.argv) != 4:
        print("python main.py <provenance graph file> <query graph file> <threshold>")
        exit(1)
    provenance_graph_file = sys.argv[1]
    threshold = int(sys.argv[3])
    print("Calling score function on file: {}".format(provenance_graph_file))
    create_list_of_process_nodes(provenance_graph_file)
    # test computation of influence score.
    # compute_influence_score(3265251, 3265261, threshold, provenance_graph_file)
    # use the same threshold of 3 for influence score.
    query_graph_file = sys.argv[2]
    print("Using query graph file: {}".format(query_graph_file))
    num_nodes = len(get_all_nodes_in_graph(query_graph_file))
    for i in range(0, num_nodes):
        graph_alignment = find_graph_alignment(query_graph_file, provenance_graph_file,
                                      threshold, i)
        print("Final node alignment: {}".format(graph_alignment))
        alignment_score = compute_alignment_score(query_graph_file, provenance_graph_file,
                                        graph_alignment, threshold)
        print("Alignment score of the node alignment: {0:0.6f}".format(alignment_score))
        if alignment_score >= 1.0/float(threshold):
            print("Alert! Attacker may be present.")
            break
        else:
            print("Could not find attacker, trying again with another seed node...")
    print("Attacker may not be present in the system.")


