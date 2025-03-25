from causeDiscovery.CauseDiscovery import CauseDiscovery
from queryUtils import *
import time
from causeDiscovery.CausalPair import CausalPair


class EffectiveCD(CauseDiscovery):
    def __init__(self, **kwargs):
        super(EffectiveCD, self).__init__(**kwargs)
        self.independent_queue = []
        self.remained_variables = set()
        self.get_variables(self.file_path)

    def variables_to_str(self, variables):
        ret = ""
        for v in variables:
            ret += v
            ret += "\n"
        return ret

    def init_stage(self):
        print(self.variables)
        print()
        variables_str = self.variables_to_str(self.variables)
        prompt = f"你是一位电网变压器故障诊断领域专家的有力助手。下列的特征是电网变压器故障诊断领域的关键变量，它们之间存在丰富的因果关系。"\
            "你的目标是在这些变量之间构造一个因果图谱。\n "\
            f"{variables_str}"\
            "现在你需要使用这些数据构造一个因果图谱。你将首先识别出这些变量中不被其它任何变量所影响的变量，最多不超过7个。一步一步地思考。接着通过<Answer>...</Answer>标签提供你的答案（只包含变量的名字)。"


        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        print(response)
        response = response.choices[0].message.content.split("\n")

        start_tag = False
        end_tag = False
        for line in response:
            if end_tag:
                break

            if line.strip() == "</Answer>":
                end_tag = True
            elif start_tag:
                self.independent_queue.append(line.strip())
            elif line.strip() == "<Answer>":
                start_tag = True

        print(self.independent_queue)
        # 将剩下的变量放入其中
        for v in self.variables:
            if v not in self.independent_queue:
                self.remained_variables.add(v)
        print()
        print(self.remained_variables)

    def expansion_stage(self):
        if len(self.independent_queue) == 0:
            print("error,independent_queue is empty.")

        print(self.independent_queue)
        print(self.remained_variables)
        print()

        current_node = self.independent_queue.pop(0)

        # 获取关系，并转化成标准格式
        pc_edges = self.edges_PC()
        pc_edges_str = ""

        for parent, children in pc_edges.items():
            pc_edges_str = pc_edges_str + parent + "导致"
            for child in children:
                pc_edges_str += child
                pc_edges_str += '，'

            pc_edges_str = pc_edges_str[:-1]
            pc_edges_str += '\n'

        remained_variables_str = ""
        for v in self.remained_variables:
            remained_variables_str = remained_variables_str + v + "\n"

        prompt = f"已知{current_node}是不受其它任何变量影响的节点，同时有以下的因果关系：\n" \
                 f"{pc_edges_str}" \
                 f"从下列的变量中选择选择受到{current_node}影响的变量，最多不超过7个。\n" \
                 f"{remained_variables_str} " \
                 "一步一步的思考。接着通过<Answer>...</Answer>标签提供你的答案（只包含变量的名字)。"

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        response = response.choices[0].message.content.split("\n")

        start_tag = False
        end_tag = False
        for line in response:
            if end_tag:
                break

            if line.strip() == "</Answer>":
                end_tag = True
            elif start_tag:
                self.independent_queue.append(line.strip())
                self.edges.add(CausalPair(current_node, line.strip()))
                if line.strip() in self.remained_variables:
                    self.remained_variables.remove(line.strip())
            elif line.strip() == "<Answer>":
                start_tag = True

    def run(self):
        self.start_time = time.time()
        self.get_variables(self.file_path)

        self.init_stage()
        round = 0
        while len(self.remained_variables) != 0 and len(self.independent_queue) != 0:
            self.expansion_stage()
            print(f"round:{round}")
            round += 1

        self.end_time = time.time()
        print(f"耗时:{self.end_time - self.start_time}")
        self.write_pair()
        self.write_json()


if __name__ == '__main__':
    effective_cd = EffectiveCD(file_path="D:\cause_analyse\llamaProject\static\\files\\variables.txt")
    effective_cd.run()
