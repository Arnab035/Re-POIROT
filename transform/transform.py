import sys
from collections import OrderedDict

event_type = {'a': 1,  # process
       'b': 2,  # thread
       'c': 3, # file
       'd': 4, # MAP_ANONYMOUS
       'e': 5, # NA
       'f': 6,   # stdin
       'g': 7,   # stdout
       'h': 8,   # stderr
       'i': 9,   # accept
       'j': 10,   # access
       'k': 11,     # bind
       'l': 12,    # chmod
       'm': 13,    # clone
       'n': 14,    # close
       'o': 15,  # connect
       'p': 16,   # execve
       'q': 17,    # fstat
       'r': 18, # ftruncate
       's': 19,   # listen
       't': 20,    # mmap2
       'u': 21,     # open
       'v': 22,     # read
       'w': 23,     # recv
       'x': 24,  # recvfrom
       'y': 25,   # recvmsg
       'z': 26,      # send
       'A': 27,   # sendmsg
       'B': 28,    # sendto
       'C': 29,      # stat
       'D': 30,  # truncate
       'E': 31,    # unlink
       'F': 32,   # waitpid
       'G': 33,     # write
       'H': 34,    # writev
      }

# vertex_type : dict {vertex-id: vertex-type, vertex-type is one
#                     of the alphabets above}

if __name__ == "__main__":
    vertex_type = {}
    edge_type = {} # dict of int & set of tuples
    with open(sys.argv[1], 'r') as f:
        for line in f:
            entry = line.split()
            # ['3942233', '3944514', 'a:c:n:0:0:253127']
            # print(int(entry[0])),
            # print(entry[2].split(':')[0]),
            # print(int(entry[1])),
            object_types = entry[2].split(':')
            vertex_type[int(entry[0])] = object_types[0]
            vertex_type[int(entry[1])] = object_types[1]
            # vertex_type[int(entry[0])] = entry[2].split(':')[0]
            if int(entry[0]) in edge_type:
                edge_type[int(entry[0])].add((int(entry[1]), object_types[2]));
            else:
                edge_type[int(entry[0])] = set()
    #print(edge_type)
    print("Number of vertices is: {}".format(len(vertex_type)))
    keys = list(vertex_type.keys())
    keys.sort()
    sorted_vertex_type = OrderedDict()
    for i in keys:
        sorted_vertex_type[i] = vertex_type[i]

    normalized_vertex_type = {}
    index = 0
    for vertex_id in sorted_vertex_type:
        normalized_vertex_type[vertex_id] = index
        index = index + 1
    # debug
    #for vertex_id, v_type in normalized_vertex_type.items():
    #    print("{} {}".format(vertex_id, v_type))

    modified_vertex_type = {}
    for vertex_id, norm in normalized_vertex_type.items():
        modified_vertex_type[norm] = event_type[sorted_vertex_type[vertex_id]]

    for vertex_id, v_type in modified_vertex_type.items():
        print("{} {}".format(vertex_id, v_type))

    modified_edge_type = {}
    for edge_id, edge_val in edge_type.items():
        modified_edge_id = normalized_vertex_type[edge_id]
        modified_edge_type[modified_edge_id] = set()
        for edg_val in edge_val:
            modified_edge_type[modified_edge_id].add((normalized_vertex_type[edg_val[0]], event_type[edg_val[1]]))
    
    # debug
    #for modified_edge_id, modified_edge_vals in modified_edge_type.items():
    #    for modified_edge_val in modified_edge_vals:
            #print("{} {} {}".format(modified_edge_id, modified_edge_val[0], modified_edge_val[1]))
  
    e_keys = list(modified_edge_type.keys())
    e_keys.sort()
    sorted_modified_edge_type = OrderedDict()
    for i in e_keys:
        sorted_modified_edge_type[i] = modified_edge_type[i]
    
    # debug
    #for sorted_modified_edge_id, sorted_modified_edge_vals in sorted_modified_edge_type.items():
    #    for sorted_modified_edge_val in sorted_modified_edge_vals:
    #        print("{} {} {}".format(sorted_modified_edge_id, sorted_modified_edge_val[0], 
    #            sorted_modified_edge_val[1]))
    
    for i in range(0, len(vertex_type)):
        if i not in sorted_modified_edge_type:
            print(0)
        else:
            sorted_modified_edge_vals = sorted_modified_edge_type[i]
            for sorted_modified_edge_val in sorted_modified_edge_vals:
                print("{} {} {}".format(i, sorted_modified_edge_val[0],
                        sorted_modified_edge_val[1]))
