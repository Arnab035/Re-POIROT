import sys
from scores import *

if __name__ == "__main__":
    print("Starting Poirot...")
    print("Calling score function on file: {}".format("base-download-v2-400.txt"))
    create_list_of_process_nodes("base-download-v2-400.txt")
    compute_influence_score(3267272, 3269876, 3, "base-download-v2-400.txt")
