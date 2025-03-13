from abc import abstractmethod
import time
import openai
from normalUtils import *

class CauseDiscovery():
    file_path = ''
    variables = set()
    start_time = 0
    end_time = 0
    edges = set()
    parent_children = {}
    child_parents = {}

    def __init__(self, file_path, output_path='./output.txt'):
        self.file_path = file_path
        self.output_path = output_path
        self.client = openai.OpenAI(api_key="sk-9a9e275dad9d4e40b3aefc27bed0c27c", base_url="https://api.deepseek.com")

    def get_variables(self, file_path):
        encoding = get_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            line = line.strip()
            self.variables.add(line)

    def show_variables(self):
        print(self.variables)

    def edges_PC(self):
        self.parent_children.clear()
        for edge in self.edges:
            parent = edge.parent
            child = edge.child

            if parent not in self.parent_children:
                self.parent_children[parent] = []
            self.parent_children[parent].append(child)

        return self.parent_children

    def edges_CP(self):
        self.child_parents.clear()
        for edge in self.edges:
            parent = edge.parent
            child = edge.child

            if child not in self.child_parents:
                self.child_parents[child] = []
            self.child_parents[child].append(parent)

        return self.child_parents

    def write_pair(self, path="./output_pair.txt"):
        with open(path, 'w') as f:
            for edge in self.edges:
                parent = edge.parent
                child = edge.child
                f.write(f"{parent}->{child}")
                f.write("\n")
        f.close()

    def write_json(self, path="./output_json.json"):
        if len(self.child_parents) == 0:
            self.edges_CP()

        result = {}
        for child, parents in self.child_parents.items():
            result[child] = {
                "name": child,
                "parents": parents
            }

        with open(path, 'w') as f:
            f.write(json.dumps(result, indent=2, ensure_ascii=False))
        f.close()


    @abstractmethod
    def run(self):
        pass

if __name__ == '__main__':
    cd = CauseDiscovery()
    cd.get_variables(f"./static/files/variables.txt")
    cd.show_variables()