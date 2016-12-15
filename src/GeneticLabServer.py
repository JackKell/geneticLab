from pysyncobj import SyncObj
from pysyncobj import replicated


class GeneticLabServer(SyncObj):
    def __init__(self):
        super(GeneticLabServer, self).__init__('localhost:1337', [])
        self.cannonResults = []

    @replicated
    def __saveResult(self, results):
        pass

    @replicated
    def runSimulation(self):
        pass

    def run(self):
        pass
