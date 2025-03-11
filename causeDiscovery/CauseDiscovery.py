from abc import abstractmethod

import openai
from normalUtils import *

class CauseDiscovery():
    file_path = ''
    output_path = './output.txt'
    variables = set()

    def __init__(self, file_path, output_path):
        self.file_path = file_path
        self.output_path = output_path

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

    @abstractmethod
    def run(self):
        pass

if __name__ == '__main__':
    cd = CauseDiscovery()
    cd.get_variables(f"./static/files/variables.txt")
    cd.show_variables()