import sys
import time
from scores import *
from utils import *


if __name__ == "__main__":
    print("Starting Poirot...")
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print("python main.py <provenance graph file> <query graph file> <threshold> <parallel (optional)>")
        exit(1)
    provenance_graph_file = sys.argv[1]
    threshold = int(sys.argv[3])
    is_parallel = False
    if len(sys.argv) == 5:
        is_parallel = True
    print("Calling score function on file: {}".format(provenance_graph_file))
    create_list_of_process_nodes(provenance_graph_file)
    # test computation of influence score.
    # compute_influence_score(3265251, 3265261, threshold, provenance_graph_file)
    # use the same threshold of 3 for influence score.
    query_graph_file = sys.argv[2]
    print("Using query graph file: {}".format(query_graph_file))
    num_nodes = len(get_all_nodes_in_graph(query_graph_file))
    if is_parallel:
        import parallel_algorithm as p_data
        for i in range(0, num_nodes):
            start = time.time()
            p_data.find_graph_alignment(query_graph_file, provenance_graph_file,
                                        threshold, i)
            print("Final node alignment: {}".format(p_data.aligned_nodes))
            alignment_score = compute_alignment_score(query_graph_file, provenance_graph_file,
                                        p_data.aligned_nodes, threshold)
            print("Alignment score of the node alignment: {0:0.6f}".format(alignment_score))
            end = time.time()
            print("Time taken to run: {}".format(end - start))
            if alignment_score >= 1.0/float(threshold):
                print("Alert! Attacker may be present.")
                sys.exit()
            else:
                print("Could not find attacker, trying with another seed node...")
    else:
        import algorithm as data
        for i in range(0, num_nodes):
            start = time.time()
            graph_alignment = data.find_graph_alignment(query_graph_file, provenance_graph_file,
                                      threshold, i)
            print("Final node alignment: {}".format(graph_alignment))
            alignment_score = compute_alignment_score(query_graph_file, provenance_graph_file,
                                        graph_alignment, threshold)
            print("Alignment score of the node alignment: {0:0.6f}".format(alignment_score))
            end = time.time()
            print("Time taken to run: {}".format(end - start))
            if alignment_score >= 1.0/float(threshold):
                print("Alert! Attacker may be present.")
                sys.exit()
            else:
                print("Could not find attacker, trying again with another seed node...")
    print("Attacker may not be present in the system.")

    # uncomment the below code to perform memory analysis of POIROT
    '''
    print("Now doing memory analysis...for the first round of POIROT")
    import algorithm as data
    from memory_profiler import memory_usage
    mem_usage = memory_usage((data.find_graph_alignment, (query_graph_file, provenance_graph_file, threshold, 0)), \
                            interval = 1)
    print("Average memory consumed: {} MB".format(sum(mem_usage)/float(len(mem_usage))))
    '''
