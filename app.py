from flask import Flask, request, make_response
from ollama import chat
from flask_cors import CORS
import tools
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def hello_world():
    return 'Hello, World!'

from flask import request

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/answer', methods=['POST'])
def generateAnswer():
    question = request.get_json().get('question')
    chatResponse = chat(model='llama3.2', messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    print(chatResponse['message']['content'])
    return chatResponse['message']['content']

@app.route("/testCORS", methods=['POST'])
def testCORS():
    response = make_response({"message": "Graph generated successfully!"})
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有来源的请求
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'  # 允许的方法
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # 允许的请求头
    return response

@app.route('/generate/graph', methods=['POST'])
def generateGraph():
    # 输入数据集Data
    data = request.get_json().get('data')
    print(data)

    edges = data.split('\n')  # 将字符串按行分割，每一行代表一个边
    nodes = {}
    links = []

    for edge in edges:
        if edge.strip():  # 排除空行
            node1, node2 = edge.strip('<>').split(',')  # 分离边中的两个节点
            # 添加节点到字典，确保每个节点只添加一次
            if node1 not in nodes:
                nodes[node1] = len(nodes)
            if node2 not in nodes:
                nodes[node2] = len(nodes)
            # 添加链接（边）
            links.append({'source': nodes[node1], 'target': nodes[node2]})

    # Step 2: 构建节点列表
    node_list = [{'id': str(idx), 'name': name, 'category': idx} for name, idx in nodes.items()]

    # Step 3: 构建分类列表（去重后的节点）
    categories = [{'name': name} for name in nodes]

    # Step 4: 构建最终的 JSON 数据结构
    graph_data = {
        'nodes': node_list,
        'links': links,
        'categories': categories
    }



    response = make_response({"data": graph_data})
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有来源的请求
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'  # 允许的方法
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # 允许的请求头
    return response

    # return {
    #     "nodes": [
    #         {
    #             "id": "0",
    #             "name": "发热",
    #             "category": 0,
    #             "x": 100,
    #             "y": 200,
    #             "symbolSize": 19.12381,
    #         },
    #         {
    #             "id": "1",
    #             "name": "高电压",
    #             "category": 1,
    #             "x": 200,
    #             "y": 100,
    #             "symbolSize": 19.12381,
    #         },
    #         {
    #             "id": "2",
    #             "name": "冷却设备故障",
    #             "category": 2,
    #             "x": 20,
    #             "y": 100,
    #             "symbolSize": 19.12381,
    #         },
    #         {
    #             "id": "3",
    #             "name": "声音异常",
    #             "category": 3,
    #             "x": 200,
    #             "y": 140,
    #             "symbolSize": 19.12381,
    #         },
    #     ],
    #     "links": [
    #         {
    #             "source": "1",
    #             "target": "0"
    #         },
    #         {
    #             "source": "2",
    #             "target": "0"
    #         },
    #         {
    #             "source": "0",
    #             "target": "3"
    #         },
    #     ],
    #     "categories": [
    #         {
    #             "name": "发热"
    #         },
    #         {
    #             "name": "高电压"
    #         },
    #         {
    #             "name": "冷却设备故障"
    #         },
    #         {
    #             "name": "声音异常"
    #         }
    #     ]
    # }

@app.route('/getChain', methods=['POST'])
def getChain():
    str = request.get_json().get('query')
    return tools.getChain(str)

if __name__ == '__main__':
    app.run(debug=True)