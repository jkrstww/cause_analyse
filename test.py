from openai import OpenAI
from normalUtils import get_encoding
import json

client = OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

encoding = get_encoding('./static/files/datasets/samples.json')
with open('./static/files/datasets/samples.json', 'r', encoding=encoding) as f:
    dict = json.load(f)
f.close()

output_dict = {}
i = 1
for key, value in dict.items():
    symptom = value["故障表现"]

    answer = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "你是变压器故障诊断方面的专家，现在你需要根据以下的变压器故障的症状，分析其背后的根本原因，并给出建议。"},
            {"role": "user", "content": symptom}
        ]
    ).choices[0].message.content
    output_dict[symptom] = answer
    print(answer)

    print(i)
    i += 1

write_dict = {}
i = 0
for item in output_dict.items():
    i += 1
    write_dict[f"案例{i}"] = item

print(write_dict)

with open('./normal_output.json', 'a+') as f:
    f.write(json.dumps(write_dict))
f.close()