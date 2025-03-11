import ollama
import openai

# answer = ollama.generate(model='deepseek-r1', prompt='你是谁')
# print(ollama.list())
#
# res1 = ollama.chat(model='deepseek-r1', messages=[{'role': 'user', 'content': '你是谁'}])
# print(res1.message.content)
# res2 = ollama.chat(model='deepseek-r1', messages=[{'role': 'user', 'content': '你到底是谁'}])
# print(res2.message.content)


client = openai.OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "你是电网领域和大型语言模型领域的专家。"},
        {"role": "user", "content": "阅读以下文本，并基于你对大模型图推理技术的理解，思考如何使用该技术提高电网应急管理的决策准确性与响应速度：在此基础上，本课题选取适用于电力与应急管理领域的预训练语言模型（如BERT、GPT等），并进行领域适配，以提高模型对电网特定术语与语境的理解能力。同时，结合文本、图像（如设备状态图）、表格（历史数据记录）等多模态数据，运用跨模态学习技术，实现对电网应急信息的全面理解与表征。研究利用图神经网络（Graph Neural Network, GNN）对构建的知识图谱进行编码与推理。GNN能够有效捕捉图中节点与边的特征信息，通过消息传递机制使图中的节点相互更新自身信息，形成准确的推理结果。例如，面对新设备故障的信息输入，GNN可根据故障性质与历史响应数据推导出最佳应急响应策略。"},
    ],
    stream=False
)

print(response.choices[0].message.content)