import collections
import gzip
import re
import timeit
import networkx as nx
import os

def sam_read(sam_file):    #read sequence ID from SAM file.
    reads = []
    with open(sam_file) as f:
        for line in f:
            str_list = line.split()
            head = str_list[0]
            if '@' not in head[0]:
                reads.append(str_list[0])

    return reads

filename = 'test_new.gz'
samfile = 'test_new.sam'
reads = sam_read(samfile)

G = nx.Graph()
finish_node = []
while reads != []:
    with gzip.open(filename, 'rt') as file:

        reads_new = []
        string_line = (line.split() for line in file)
        edge_list = ((item[1], item[2]) for item in string_line if (item[1] in reads or item[2] in reads))

        G.add_edges_from(edge_list)
        reads_new = list(G)
        print('reads: ' + str(reads))
        print('reads_new: ' + str(reads_new))

        for node in reads:
            # reads_new.remove(node)
            finish_node.append(node)

        for node in finish_node:
            reads_new.remove(node)

        print('reads after delete: ' + str(reads_new) + '\n')

        reads = reads_new


print(list(G))
print(len(list(G)))
