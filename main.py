import os

import queryUtils
from fileUtils import *
from normalUtils import *
from ollamaUtils import *
from queryUtils import *

nodes = get_variables('./static/files/variables.txt')

# triplet_set = get_triplets(nodes)
# candidate_edges = []
# for triplet in triplet_set:
#     directional_triplet = get_subgraph(triplet)
#     print(directional_triplet)
#     for edge in directional_triplet:
#         print(edge)
#         candidate_edges.append(edge)
# print(candidate_edges)
# print(merge_subgraph(nodes, candidate_edges))

# response = queryUtils.variables_to_graph(nodes, mode="direct")
# print(response)
#
# with open("test1.txt", 'w') as f:
#     f.write(response)


# with open("test2.txt", 'w') as f:
#     round = 1
#     for node in nodes:
#         response = variable_to_graph_pairs(node, nodes)
#         f.write(response)
#         print(round)
#         round += 1
# f.close()

files = os.listdir("./static/files/reference")
with open('test3.txt', 'w') as F:
    for file in files:
        path = "./static/files/reference/" + file
        encoding = get_encoding(path)
        with open(path, 'r', encoding=encoding) as f:
            txt = f.readlines()
            response = txt_to_graph(txt)
            F.write(response)
        f.close()
F.close()