import collections
import gzip
import re
import timeit
import networkx as nx
import os


def read_gz(filename):
    edge_list = []
    with gzip.open(filename, 'rt') as f:
        for line in f:
            if bool(re.findall(r"ED.*", line)):
                str_list = line.split()
                node1 = str_list[1]
                node2 = str_list[2]
                edge_list.append((node1, node2))
    return edge_list

def node_list(edge_list):
    dict = collections.defaultdict(list)
    for edge in edge_list:
        dict[edge[0]].append(edge)
    return dict

def sam_read(sam_file):    #read sequence ID from SAM file.
    reads = []
    with open(sam_file) as f:
        for line in f:
            str_list = line.split()
            head = str_list[0]
            if '@' not in head[0]:
                reads.append(str_list[0])

    return reads

def get_edges(node_dict, reads):
    edge_list = []
    new_reads = []
    for node in reads:
        collect = node_dict[node]
        if collect != []:
            for item in collect:
                edge_list.append(item)
                new_reads.append(item[1])
        else:
            continue
    return edge_list, new_reads

def final_result(edge_list):
    G = nx.DiGraph()
    for edge in edge_list:
        node1 = edge[0]
        node2 = edge[1]
        G.add_edges_from([(node1, node2)])

    roots = list(v for v, d in G.in_degree() if d == 0)
    leaves = list(v for v, d in G.out_degree() if d == 0)

    all_paths = []
    for root in roots:
        for leaf in leaves:
            paths = nx.all_simple_paths(G, root, leaf)
            all_paths.extend(paths)

    return all_paths

def save_result(all_paths):
    cwd = os.getcwd()
    textFile = cwd + '/PATH-split.txt'
    file = open(textFile, 'w+')
    for i in all_paths:
        file.write(','.join([j for j in i]) + "\n")
    file.close()
    return

def get_gz():       # find out all the split ed file in cwd
    path = os.getcwd()
    ed_split = []
    for filename in os.listdir(path):
        ed_split += re.findall('ed.split.*', filename)
    return ed_split


time_start = timeit.default_timer()

print('loading sam file......')
reads = sam_read('test.sam')
print('loading complete.')
print('finding out all the split gz file......')
all_gz_file = get_gz()
print('all split get.')

result = []
count = 0

print('iteration search start.\n')
while reads != []:
    new_input = []

    for filename in all_gz_file:
        ed = read_gz(filename)
        node_dict = node_list(ed)
        edge, new = get_edges(node_dict, reads)
        result.extend(edge)
        new_input.extend(new)

    reads = new_input
    count = count + 1

    print('iteration ' + str(count) + ' complete.')
    print( str(len(reads)) + ' nodes remains for next round.')

print('computing result....')
final_path = final_result(result)
save_result(final_path)
print('check the result in the PATH-split.txt')
time_end = timeit.default_timer()
print('total time is: '+ str(time_end - time_start) + 's')
