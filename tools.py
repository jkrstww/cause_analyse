import difflib


def load_knowledge(file_path):
    """
    从 knowledge.txt 文件中加载知识图谱并返回正向图。
    正向图的键是节点，值是该节点指向的节点列表。
    """
    graph = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                # 提取两个节点，格式为 <a, b> -> b 指向 a
                node1, node2 = line[1:-1].split(', ')
                if node2 not in graph:
                    graph[node2] = []
                graph[node2].append(node1)
    return graph


def find_best_match(phrase, nodes):
    """
    在节点列表中找到与短语最相似的节点。
    使用 difflib 的 get_close_matches 方法来计算相似度。
    """
    matches = difflib.get_close_matches(phrase, nodes, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    return None


def build_forward_path(description, graph):
    """
    根据描述（description）中的短语，沿着知识图谱构建路径。
    """
    nodes = list(graph.keys())  # 获取图中的所有节点
    phrases = description.split(',')  # 假设每个短语由空格分开
    path = []

    # 遍历每个短语，找到最相似的节点
    for phrase in phrases:
        best_match = find_best_match(phrase, nodes)
        if best_match:
            path.append(best_match)
        else:
            continue

    # 沿着路径构建正向路径
    result = []
    visited = set()

    for start_node in path:
        if start_node in visited:
            break  # 如果已经访问过该节点，跳过
        current_node = start_node
        path_str = current_node
        visited.add(current_node)

        while current_node in graph and graph[current_node]:
            next_node = graph[current_node][0]  # 假设每个节点只指向一个节点
            if next_node in visited:
                break  # 遇到重复节点，停止
            path_str = path_str + "<-" + next_node  # 构建路径
            visited.add(next_node)
            current_node = next_node

        result.append(path_str)

    return "\n".join(result)


# 主函数
def getChain(description):
    # 加载知识图谱
    knowledge_file = 'knowledge.txt'
    graph = load_knowledge(knowledge_file)

    # 根据描述构建正向路径
    path = build_forward_path(description, graph)

    # 输出结果
    return path




