from causeDiscovery.CausalPair import CausalPair
from causeDiscovery.CauseDiscovery import CauseDiscovery
import time

class PairCD(CauseDiscovery):
    def __init__(self, **kwargs):
        super(PairCD, self).__init__(**kwargs)

    def compare(self, a, b):
        prompt = f"你是电网变压器诊断领域的专家，现在给定两个变量: \
        {a},{b}，直接给出二者的因果顺序，用->隔开。"

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        response = response.choices[0].message.content
        line = response.strip().replace(" ", "").split("->")
        self.edges.add(CausalPair(line[0], line[1]))

    def run(self):
        self.start_time = time.time()
        self.get_variables(self.file_path)

        v_list = list(self.variables)
        length = len(v_list)

        round = 0
        for i in range(length):
            for j in range(i+1, length):
                self.compare(v_list[i], v_list[j])
                print(f"round:{round}")
                round += 1

        self.write_pair()
        self.write_json()

        self.end_time = time.time()
        print(f"耗时:{self.end_time-self.start_time}")
        self.write_pair()
        self.write_json()

if __name__ == '__main__':
    effective_cd = PairCD(file_path="D:\cause_analyse\llamaProject\static\\files\\variables.txt")
    effective_cd.run()
