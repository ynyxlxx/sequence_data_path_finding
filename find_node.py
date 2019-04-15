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

def save_result(node_list):
    cwd = os.getcwd()
    textFile = cwd + '/node.txt'
    file = open(textFile, 'w+')
    for i in node_list:
        file.write(''.join(i) + "\n")
    file.close()
    return


time_start = timeit.default_timer()

filename = 'E:/DIrection study/E.coil/ed-ecoli.gz'
samfile = 'E:/DIrection study/E.coil/ecoli2_and_lambda_mappedindex.sam'
reads = sam_read(samfile)

node_dict = collections.defaultdict(list)

with gzip.open(filename, 'rt') as file:
    string_line = (line.split() for line in file)
    edge_list = ((item[1], item[2]) for item in string_line)

    for edge in edge_list:
        node_dict[edge[0]].append(edge[1])


already_seen = []

while reads != []:

    reads_new = []
    collect = (node_dict[node] for node in reads if node not in already_seen)
    if collect != []:
        for item in collect:
            for next_node in item:
                already_seen.append(next_node)
                reads_new.append(next_node)

    reads = reads_new

result = []
temp = (node for node in node_dict)
for x in temp:
    result.append(x)
    result.extend(node_dict[x])
result = list(set(result))


print('saving result....')
save_result(result)
time_end = timeit.default_timer()
print('save complete.')
print('total time is: '+ str(time_end - time_start) + 's')
# print(list(node_dict))
# print(node_dict)
# print(already_seen)
















# finished_node = []
# while reads != []:
#     with gzip.open(filename, 'rt') as file:
#
#         reads_new = []
#         string_line = (line.split() for line in file)
#         edge_list = ((item[1], item[2]) for item in string_line if (item[1] in reads or item[2] in reads))
#
#         graph = node_list(edge_list)
#         reads_new = list(graph)
#         print('reads: ' + str(reads))
#         print('reads_new: ' + str(reads_new))
#
#         for node in reads:
#             finished_node.append(node)
#
#         for node in finished_node:
#             reads_new.remove(node)
#
#         print('reads after delete: ' + str(reads_new))
#         print('nodes finish: ' + str(finished_node) + '\n')
#
#         reads = reads_new


