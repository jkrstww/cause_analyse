import openai

def variables_to_graph(nodes, mode):
    if mode == 'direct':
        prompt = f"你是电力变压器故障诊断领域的专家，请根据输入的词语列表，按照以下规则分析并输出直接的因果关系对：\
        1. **因果判断原则**：原因必须直接触发结果，符合变压器领域的逻辑\
        2. **分析步骤**：\
           a) 识别每个词语的实际含义和使用场景\
           b) 按'原因→结果'顺序寻找两个词语间的强逻辑关系\
           c) 排除间接关联（如'感冒→吃药'需经过'看病'环节则不直接成立）\
        3. **输出要求**：用箭头符号'->'连接因果对，结果以['原因->结果', ...]格式呈现\
        示例：\
        输入：['吃饭','看病','肚子饿','感冒','吃药']\
        输出：['肚子饿->吃饭', '感冒->看病', '看病->吃药']\
        现在请处理这个输入列表：\
        输入：{str(nodes)}\
        输出："

        client = openai.OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        return response.choices[0].message.content

def variable_to_graph_pairs(node, nodes):
    prompt = f"**任务说明**：\
    你是变压器故障诊断领域的专家，请根据给定的目标变量和候选结果列表，精确识别目标变量直接引发的所有结果项，按以下规则生成因果关系链：\
    **输入格式**：\
    - 目标变量：[变量名称]\
    - 候选列表：[结果项1, 结果项2,...]\
    **处理规则**：\
    1. **因果方向**：仅保留'变量→结果'的单向关系，排除反向或无关项\
       - 正确示例：'感冒→看病'（疾病导致就医行为）\
       - 错误示例：'看病→感冒'（违反因果关系）\
    2. **直接性验证**：\
       a) 结果必须由变量直接触发，无需中间步骤\
       b) 排除二级传导结果（如'感冒→免疫系统激活→退烧'仅保留首层）\
    3. **语义关联强度**：\
       a) 必须符合常识逻辑（如疾病类变量应关联医疗行为）\
       b) 排除弱关联（如'感冒→吃饭'需有明确因果逻辑才保留）\
    **分析步骤**：\
    1. 解析目标变量的核心语义（如'感冒'代表呼吸道疾病）\
    2. 对候选列表逐项执行：\
       a) 判断是否存在直接因果关系（变量是否为结果的充分条件）\
       b) 验证是否符合领域常识（医疗领域、生活常识等）\
    3. 生成标准化输出\
    **示例演示**：\
    输入：\
    变量：感冒\
    候选列表：['吃饭','看病','肚子饿','看医生','吃药']\
    输出：\
    ['感冒->看病', '感冒->看医生', '感冒->吃药']\
    **异常处理**：\
    - 当候选列表出现歧义项时（如'买药'），优先选择最直接关联项\
    - 对同义词合并处理（如'看病'与'看医生'同时存在时均保留）\
    请处理以下输入：\
    变量：{str(node)}\
    候选列表：{str(nodes)}\
    输出："

    client = openai.OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    return response.choices[0].message.content