from itertools import combinations
import re
import chardet
import json

def get_triplets(variables):
    # 使用 combinations 生成所有长度为3的组合
    triplets_list = list(combinations(variables, 3))
    return triplets_list

def match_tag(text, tag):
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return ''

def init_edge_dict(node_set):
    dict = {}
    for i in range(len(node_set)):
        for j in range(i + 1, len(node_set)):
            dict[f'{i},{j}'] = 0
            dict[f'{j},{i}'] = 0
    return dict

def merge_subgraph(node_set, candidate_edge):
    node_num = len(node_set)
    edge_num_dict = init_edge_dict(node_set)
    for edge in candidate_edge:
        edge_num_dict[str(edge)] += 1

    edge_set = []
    for i in range(len(node_set)):
        for j in range(i + 1, len(node_set)):
            node1 = node_set[i]
            node2 = node_set[j]
            edge12_num = edge_num_dict[str(node1) + ',' + str(node2)]
            edge21_num = edge_num_dict[str(node2) + ',' + str(node1)]
            no_edge_num = node_num - edge12_num - edge21_num - 2

            max_num = max(edge21_num, edge12_num, no_edge_num)
            if max_num == edge12_num:
                edge_set.append(str(node1) + ',' + str(node2))
            elif max_num == edge21_num:
                edge_set.append(str(node2) + ',' + str(node1))

    return edge_set

def get_encoding(file):
    with open(file,'rb') as f:
        tmp = chardet.detect(f.read())
        return tmp['encoding']

def write_json(file_path, write_path):
    edges = []
    encoding = get_encoding(file_path)
    node_map = {}

    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()
    f.close()

    if file_path == "./static/files/base.txt":
        for line in lines:
            line = line.strip().split(',')
            parent, child = line[0], line[1]
            if child not in node_map:
                node_map[child] = []
            node_map[child].append(parent)
    else:
        for line in lines:
            line = line.strip()
            if line.startswith("'") or line.startswith('"'):
                edges.append(line[1:-2])
                for edge in edges:
                    parent, child = edge.split('->')
                    if parent not in node_map:
                        node_map[child] = []
                    node_map[child].append(parent)
    # 构建最终结果字典
    result = {}
    for child, parents in node_map.items():
        result[child] = {
            "name": child,
            "parents": parents
        }

    with open(write_path, 'w') as f:
        f.write(json.dumps(result, indent=2, ensure_ascii=False))
    f.close()

def write_variables(filePath, targetPath):
    variables = set()
    encoding = get_encoding(filePath)
    with open(filePath, 'r', encoding=encoding) as F:
        lines = F.readlines()
        for line in lines:
            line = line.strip().split(',')
            head, tail = line[0], line[1]
            variables.add(head)
    F.close()

    with open(targetPath, 'w') as f:
        for variable in variables:
            f.write(variable + '\n')
    f.close()

write_json("./static/files/base.txt", "./static/files/base.json")


