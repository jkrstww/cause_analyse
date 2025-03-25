from causeDiscovery.CauseDiscovery import CauseDiscovery
from normalUtils import list_to_str
import time
from causeDiscovery.CausalPair import CausalPair

class CompareCD(CauseDiscovery):
    def __init__(self, compare_nums, **kwargs):
        super(CompareCD, self).__init__(**kwargs)
        self.compare_num1 = compare_nums[0]
        self.compare_num2 = compare_nums[1]

    def compare(self, vs1, vs2):
        vs1_str = list_to_str(vs1)
        vs2_str = list_to_str(vs2)
        prompt = f"请按照以下步骤分析输入的两个列表元素之间的因果关系：\
        1. **列表内部因果分析**：\
           首先识别list1中元素之间的直接因果关系，遵循'原因->结果'的链式结构。例如当A导致B且B导致C时，应同时保留A->B和B->C，如果两个元素间没有因果关系则不显示。\
        2. **跨列表因果推断**：\
           分析list1中每个元素如何导致list2中的每个元素，建立明确的因果关系。注意：\
           - 允许一个原因导致多个结果\
           - 允许不同原因导致相同结果\
           - 需要基于物理/工程常识判断合理性\
        3. **输出格式要求**：\
           - 每条因果关系单独成行\
           - 使用中文元素名称和箭头符号'->'连接\
           - 最终用<Answer>标签包裹所有结果\
        **输入示例**：\
        list1 = [过热, 短路, 绝缘失效]\
        list2 = [火花放电, 局部放电]\
        **输出示例**：\
        <Answer>\
        过热->绝缘失效\
        短路->过热\
        绝缘失效->火花放电\
        短路->火花放电\
        短路->局部放电\
        </Answer>\
        现在请处理以下新输入：\
        list1 = [{vs1_str}]\
        list2 = [{vs2_str}]"

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
                line = line.strip().split('->')
                print(line)
                p = line[0]
                c = line[1]
                self.edges.add(CausalPair(p, c))
            elif line.strip() == "<Answer>":
                start_tag = True
    def run(self):
        self.get_variables(self.file_path)
        self.vs = list(self.variables)

        self.start_time = time.time()

        round = 0
        for i in range(0, len(self.vs), 25):
            # 获取外层循环的当前批次（最多5个元素）
            outer_batch = self.vs[i:i + 25]
            # 计算外层批次最后一个元素的索引
            if not outer_batch:
                continue
            outer_last_index = i + len(outer_batch) - 1

            # 内层循环从该索引开始，每次取10个元素直到末尾
            for j in range(outer_last_index, len(self.vs), 40):
                inner_batch = self.vs[j:j + 40]
                # 这里可以处理内层批次，例如打印或其它操作
                self.compare(outer_batch, inner_batch)

                print(f"round:{round}")
                round += 1

        self.end_time = time.time()
        print(f"耗时:{self.end_time - self.start_time}")
        self.write_pair("./output_pair2.txt")
        self.write_json("./output_json2.json")

if __name__ == "__main__":
    compare_cd = CompareCD(file_path="D:\cause_analyse\llamaProject\static\\files\\variables.txt", compare_nums=[4, 10])
    compare_cd.run()
