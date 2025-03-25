from causeDiscovery.CauseDiscovery import CauseDiscovery


class NodesCD(CauseDiscovery):
    def __init__(self, **kwargs):
        super(NodesCD, self).__init__(**kwargs)

    def get(self):
        prompt = (f"你是电力变压器故障诊断领域的专家，请根据输入的词语列表，按照以下规则分析并输出直接的因果关系对：\
        1. **因果判断原则**：原因必须直接触发结果，符合变压器领域的逻辑\
        2. **分析步骤**：\
           a) 识别每个词语的实际含义和使用场景\
           b) 按'原因→结果'顺序寻找两个词语间的强逻辑关系\
           c) 排除间接关联（如'感冒→吃药'需经过'看病'环节则不直接成立）\
        3. **输出要求**：用箭头符号'->'连接因果对，最终用<Answer>标签包裹所有结果\
        **输入示例**：\
        ['吃饭','看病','肚子饿','感冒','吃药']\
        **输出示例**：\
        <Answer>\
        肚子饿->吃饭\
        感冒->看病\
        看病->吃药\
        </Answer>\
        现在请处理这个输入列表：\
        输入：{str(self.variables)}\
        输出：")