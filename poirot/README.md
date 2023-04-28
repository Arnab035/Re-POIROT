# Poirot implementation

This sub-directory contains code that implements the algorithm described in the Poirot paper

## How to run?

The algorithm is expected to run using both Python2 and Python3. 

Use the below command to run -

```
python main.py base-provenance-graph.txt query-graph.txt 3

```

where "base-provenance-graph.txt" is the filename of the file containing the provenance graph,
"query-graph.txt" is the filename of the file containing the query graph and
3 is the threshold, that gives the minimum number of compromise points an attacker may
choose to perform an attack.
