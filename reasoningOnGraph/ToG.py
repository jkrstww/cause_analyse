from normalUtils import get_encoding, match_tag
import json
from openai import OpenAI
import ast

class ToG():
    def __init__(self):
        self.class_name = "ToG"
        self.file_path = ""
        self.dict = dict()
        self.variables = list()
        self.N = 5
        self.reason_path = list()
        self.init_nodes = list()
        self.client = OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")
        self.question = ""

    def get_edges(self, file_path="D:\cause_analyse\llamaProject\static\\files\\base.json"):
        self.file_path = file_path
        encoding = get_encoding(self.file_path)

        with open(self.file_path, 'r', encoding=encoding) as f:
            dict = json.load(f)
        f.close()

        for key, value in dict.items():
            self.dict[value["name"]] = value["parents"]
            self.variables.append(value["name"])

    def init_stage(self):
        prompt = f'''
        # 关键要素筛选指令
        **任务说明**：根据问题描述，从候选列表中选取最多{self.N}个最直接相关元素，需严格满足以下条件：

        ## 处理规则
        1. **相关性判断标准**：
           - 必须与问题中明确提到的症状/关键词存在直接因果关系
           - 排除需要二次推理才能建立联系的间接关联项
           - 不添加列表外的元素，严格限定在给定范围内选择

        2. **筛选优先级**：
           a) 直接匹配问题关键词 > 症状并发症关联 > 病理机制关联
           b) 出现频次：同时匹配多个问题关键词的优先保留

        3. **数量控制**：
           - 上限不超过N个，下限允许0个（无符合项时）
           - 当符合项超过N个时，按列表顺序保留前N个
        
        4. **异常处理机制**:
            - 当候选元素存在同义词时（如问题用"头疼"而列表是"头痛"），视为等效
            - 若问题描述与所有候选元素均无直接关联，返回空列表
            - 遇到歧义表述时，优先选择与问题关键词字面匹配度高的元素
           
        5. **输出格式要求**：\
           - 最终用<Answer>标签包裹所有结果\

        ## 输入输出格式
        **输入示例1**：\
        {{
          "问题描述": "患者出现持续发热和皮疹，可能的诊断是什么？",
          "候选列表": ["登革热","糖尿病","紫外线过敏","系统性红斑狼疮"],
          "最大数量": 2
        }}
        **输出示例2**：\
        <Answer>["登革热","系统性红斑狼疮"]</Answer>

        **输入示例2**：\
        输入：
        {{
          "问题描述": "服务器CPU使用率飙升，可能的原因有哪些？",
          "候选列表": ["内存泄漏","DDoS攻击","数据库索引失效","硬盘故障"],
          "最大数量": 3
        }}
        **输出示例2**：\
        <Answer>["内存泄漏","DDoS攻击","数据库索引失效"]</Answer>

        请处理以下输入：
        {{
          "问题描述": {self.question},
          "候选列表": {self.variables},
          "最大数量": {self.N}
        }}
        '''

        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        response = response.choices[0].message.content
        # 去除Answer标签
        response = match_tag(response, "Answer")

        self.init_nodes = ast.literal_eval(response)
        print(type(self.init_nodes))

    def explore_state(self, temp_list):
        last_node = temp_list[-1]
        if last_node in self.dict:
            next_nodes = self.dict[last_node]
            for node in next_nodes:
                temp_list.append(node)
                self.explore_state(temp_list)
                temp_list.pop(-1)
        else:
            self.reason_path.append(temp_list)

    def beam_search(self):
        prompt = f'''
            你是电网变压器故障诊断领域的专家，现在根据问题{self.question}，结合以下的思维链{self.reason_path}，\
            从中选取最能够回答问题的一条思维链，结合该思维链以及你自己的思考，回答问题。
        '''

        print(self.reason_path)

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        response = response.choices[0].message.content

        return response

    def get_answer(self, question):
        self.question = question
        self.reason_path = list()
        self.init_stage()

        for node in self.init_nodes:
            temp_list = list()
            temp_list.append(node)
            self.explore_state(temp_list)

        answer = self.beam_search()
        print(answer)



if __name__ == "__main__":
    toG = ToG()
    toG.get_edges()
    toG.get_answer("变压器出现火花放电，可能的根本原因是什么？")