import openai
from normalUtils import *

class CauseDiscovery():
    variables_path = ''
    write_path = ''
    variables = set()

    def __init__(self):
        self.write_path = './output.txt'

    def get_variables(self, variables_path):
        encoding = get_encoding(variables_path)
        with open(variables_path, 'r', encoding=encoding) as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            line = line.strip()
            self.variables.add(line)

    def show_variables(self):
        print(self.variables)


if __name__ == '__main__':
    cd = CauseDiscovery()
    cd.get_variables(f"./static/files/variables.txt")
    cd.show_variables()