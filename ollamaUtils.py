import ollama
from sympy.physics.units import temperature

from normalUtils import match_tag
import ast


def get_subgraph(triplet):
    prompt = (f"找出给定的节点间的因果关系，以列表的形式，输出结果，列表中每个元素都是一条有向边。所需的输出应采用以下格式：<Answer>['A,B','B,C']</Answer>。\
    其中第一个元素表示从节点1到节点2的有向边，第二个元素表示从节点2到节点3的有向边。\
    如果一个节点不应该与其他节点形成任何因果关系，那么你可以将其添加为孤立节点。例如，如果节点3应该是孤立的节点，则结果表示应如下所示<Answer>['A,B','C']</Answer>。\
    直接使用节点的原名，不进行缩写，不要进行翻译。\
    举例1 \
    输入: ['生病','看医生','吃药']\
    输出: <Answer>['生病,看医生','看医生,吃药']</Answer>\
    举例2 \
    输入: 节点: ['下雨','打伞','写作业']\
    输出: <Answer>['下雨,打伞','写作业']</Answer>\
    举例3 \
    输入: ['疲惫','睡觉','上班']\
    输出: <Answer>['上班,疲惫','疲惫,睡觉']</Answer>\
    根据输入不要思考，直接给出答案:\
    输入: {triplet} ")

    response = ollama.generate(prompt=prompt, model='deepseek-r1').response
    print(response)
    answer = match_tag(response, 'Answer')
    print(answer)

    # 将字符串转化为对象
    elements = ast.literal_eval(answer)
    # 过滤孤立节点
    return [item for item in elements if ',' in item]

