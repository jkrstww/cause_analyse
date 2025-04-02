# 针对samples.json
import json
import re

from openai import OpenAI
from normalUtils import get_encoding

# qwen
api_key = "sk-851e06a3453b4ea6ab720de65cc33fc0"
client = OpenAI(api_key=api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

sample_dict = dict()
sample_list= []
sample_path = "../static/files/datasets/samples.json"
encoding = get_encoding(sample_path)

with open(sample_path, 'r', encoding=encoding) as f:
    samples = json.load(f)
f.close()

for key, value in samples.items():
    sample_dict[value["故障表现"]] = value["故障原因"]
    sample_list.append(value["故障原因"])

generate_dict = dict()
generate_list= []
generate_path = "../reasoningOnGraph/output.json"
encoding = get_encoding(generate_path)

with open(generate_path, 'r', encoding=encoding) as f:
    generates = json.load(f)
f.close()

for key, value in generates.items():
    generate_dict[value["故障表现"]] = value["故障原因"]
    generate_list.append(["故障原因"])

score_dict = dict()

for epoch in range(len(sample_list)):
    sample = sample_list[epoch]
    generate = generate_list[epoch]

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "请作为公正的评判者，评估以下两个由不同AI助手提供的分析的相似性。两者都收到了与机器人系统问题相关的相同数据，并被要求识别根本原因。您的工作是评估并量化两个回答之间的相似性。请通过比较两个回答并识别关键差异来开始评估。不要受回答长度的影响，不要偏袒特定助手名称，尽可能保持客观。在提供解释后，请严格按照[[评分]]格式（例如：评分：[[5]]）在1到10整数的范围内对相似性进行评分。"},
            {"role": "user", "content": f"[分析A开始]{generate}[分析A结束]\n[分析B开始]{sample}[分析B结束]"},
        ],
        stream=False
    ).choices[0].message.content
    print(response)

    pattern = '\[\[(\d+)\]\]'
    match = re.search(pattern, response, re.DOTALL)
    if match:
        score_dict[f"案例{epoch+1}"] = int(match.group(1))
    else:
        score_dict[f"案例{epoch+1}"] = 0
    print(epoch)

with open("ToG_score.json", "w") as f:
    f.write(json.dumps(score_dict))
f.close()

