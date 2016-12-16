from pysyncobj import SyncObj, replicated
from src.GeneticLabNode import GeneticLabNode
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
from threading import Thread
from queue import Queue


class GeneticLabServer(SyncObj, GeneticLabNode):
    def __init__(self, port):
        SyncObj.__init__(self, 'localhost:1337', [])
        GeneticLabNode.__init__(self, port)
        self.cannonResults = {}
        self.tcpSocket = socket()
        self.workerThreads = list()
        self.connections = Queue()

    @replicated
    def __saveResult(self, results):
        pass

    def runSimulation(self):
        pass

    def openSocket(self):
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        self.tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.tcpSocket.bind(("", self.port))
        self.tcpSocket.listen(self.backlog)

    def run(self):
        self.openSocket()
        for i in range(0, 10):
            workerThread = Thread(target=self.requestHandler)
            workerThread.start()
            self.workerThreads.append(workerThread)
        print("Running Server")
        while True:
            readyInputs, readyOutputs, readyExcepts = select([self.tcpSocket], [], [])
            for readyInput in readyInputs:
                if readyInput == self.tcpSocket:
                    self.connections.put(self.tcpSocket.accept())

    def requestHandler(self):
        while True:
            if not self.connections.empty():
                connection, address = self.connections.get()
                data = connection.recv(self.bufferSize)
                request = self.decodeMessage(data)
                print(request)
                response = self.encodeMessage({"requestType": "cannonResult"})
                connection.sendall(response)
                self.connections.task_done()


