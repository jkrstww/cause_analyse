from causeDiscovery.CauseDiscovery import CauseDiscovery
from queryUtils import *


class EffectiveCD(CauseDiscovery):
    def __init__(self, **kwargs):
        super(EffectiveCD, self).__init__(**kwargs)

    def run(self):
        self.get_variables(self.file_path)
