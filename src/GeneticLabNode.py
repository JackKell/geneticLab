from json import loads
from json import dumps
from socket import socket, AF_INET, SOCK_STREAM


class GeneticLabNode:
    def __init__(self, port):
        self.port = port
        self.timeout = 20
        self.bufferSize = 1024
        self.backlog = 25

    # Decode message takes binary data and converts it to a python dictionary
    def decodeMessage(self, binaryData):
        if type(binaryData) is tuple:
            binaryData = binaryData[0]
        receivedString = binaryData.decode("ascii")
        return loads(receivedString)

    # EncodeMessage converts python dictionary to a binary JSON formatted string
    def encodeMessage(self, dataDictionary):
        return dumps(dataDictionary).encode("ascii")

    # sends a message to the server
    def sendMessage(self, message, destinationAddress):
        tcpSocket = socket(AF_INET, SOCK_STREAM)

        tcpSocket.connect((destinationAddress, self.port))
        tcpSocket.settimeout(self.timeout)
        tcpSocket.send(message)
        data = tcpSocket.recv(self.bufferSize)

        data = self.decodeMessage(data)
        tcpSocket.close()
        return data
