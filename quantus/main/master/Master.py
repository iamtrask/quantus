__author__ = 'andrewtrask'

import zmq

from quantus.main.master.vector import Vector
from quantus.main.master.matrix import Matrix

class Master:

    LISTEN_PORT = 5555
    slaveSockets = list()
    vectors = list()
    matrices = list()

    def vector(self,length):

        vector = Vector(self.slaveSockets,length)
        self.vectors.append(vector)

        return vector

    def matrix(self, rows, cols):

        matrix = Matrix(self.slaveSockets, rows, cols)
        self.matrices.append(matrix)

        return matrix

    def addSlave(self, slavePort):

        tempSocket = self.context.socket(zmq.REQ)
        tempSocket.RCVTIMEO = 60000
        tempSocket.connect("tcp://localhost:" + str(slavePort))
        tempSocket.send(b"letMeBeYourMaster:" + str(self.LISTEN_PORT))

        try:
            response = tempSocket.recv()
            print("Slave:" + str(response))
            if (response == "yesMaster"):
                self.slaveSockets.append(tempSocket)
                return b"Added Slave on Port:" + str(slavePort)
            else:
                tempSocket.close()
                return b"Failed to add Slave on Port:" + str(slavePort) + " -- slave already has master"
        except:
            tempSocket.close()
            print("No slave listening on port:" + str(slavePort))
            return "No slave on port:" + str(slavePort)

    def countSlaves(self):

        self.controllerSocket.send(b"" + (str(len(self.slaveSockets))))


    def scanForSlaves(self):

        for i in range(20):
            self.addSlave(5556 + i)

        self.controllerSocket.send(b"Total Slaves:" + (str(len(self.slaveSockets))))

    def parseMatrixCommand(self,message):

        for slave in self.slaveSockets:
            slave.send("m")
            print(slave.recv())

        self.controllerSocket.send("performed operation")


    def parse(self, message):

        print("Received request: %s" % message)

        if (message[:9] == "addSlave:"):
            self.controllerSocket.send((self.addSlave(message[9:])))
        elif (message == "countSlaves"):
            self.countSlaves()
        elif (message == "scanForSlaves"):
            self.scanForSlaves()
        elif (message[:1] == "m"):
            self.parseMatrixCommand(message)
        else:
            self.controllerSocket.send(b"ERROR: Could not parse your command... please try again.")


    def listen(self):
        while True:
            # Wait for next request from client
            message = self.controllerSocket.recv()
            self.parse(message)

    def __init__(self):
        print("Starting Master")
        self.context = zmq.Context()
        self.controllerSocket = self.context.socket(zmq.REP)
        self.controllerSocket.bind("tcp://*:" + str(self.LISTEN_PORT))



# Send reply back to client

