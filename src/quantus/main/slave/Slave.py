__author__ = 'andrewtrask'

import time
import zmq

# from src.quantus.main.slave.subvector import SubVectorSlave

from subvector import SubVectorSlave

class Slave:
    masterAddress = "none"


    def createSubVector(self, message):
        index = len(self.subvectors)
        self.subvectors.append(SubVectorSlave(int(message)))
        return (b""+str(index))

    def add(self,index,value):
        return (b""+str(self.subvectors[index].add(value)))

    def addVec(self,index,index2):
        self.subvectors[int(index)].data += self.subvectors[int(index2)].data
        return (b"vectors added")

    def mul(self,index,value):
        return (b""+str(self.subvectors[index].mul(value)))

    def mulVec(self,index,index2):
        self.subvectors[int(index)].data *= self.subvectors[int(index2)].data
        return (b"vectors multiplied elementwise")

    def pow(self,index,value):
        return (b""+str(self.subvectors[index].pow(value)))

    def randn(self,index,value):
        return (b""+str(self.subvectors[index].randn(value)))

    def uniform(self, index, value):
        return (b""+str(self.subvectors[index].uniform(value)))

    def getData(self,index):
        return self.subvectors[int(index)].getData()

    def sum(self,index):
        return self.subvectors[int(index)].sum()

    def parseSubVectorCommand(self, message):

        if message[:7] == "create:":
            return self.createSubVector(message[7:])

        if message[:4] == "add:":
            split = int(message[4:].find(":")) + 4
            return self.add(int(message[4:split]),(message[split+1:]))

        if message[:7] == "addVec:":
            split = int(message[7:].find(":")) + 7
            return self.addVec(int(message[7:split]),(message[split+1:]))

        if message[:4] == "mul:":
            split = int(message[4:].find(":")) + 4
            return self.mul(int(message[4:split]),(message[split+1:]))

        if message[:7] == "mulVec:":
            split = int(message[7:].find(":")) + 7
            return self.mulVec(int(message[7:split]),(message[split+1:]))

        if message[:4] == "pow:":
            split = int(message[4:].find(":")) + 4
            return self.pow(int(message[4:split]),(message[split+1:]))

        if message[:6] == "randn:":
            split = int(message[6:].find(":")) + 6
            return self.randn(int(message[6:split]),(message[split+1:]))

        if message[:8] == "uniform:":
            split = int(message[8:].find(":")) + 8
            return self.uniform(int(message[8:split]),(message[split+1:]))
        
        if message[:8] == "getdata:":
            return self.getData(message[8:])

        if message[:4] == "sum:":
            return self.sum(message[4:])

        return (b"something about matrices " + message)


    def parse(self, message):
        print("Received request: %s" % message)

        if (message[:18] == "letMeBeYourMaster:"):
            if (self.masterAddress == "none"):
                self.masterAddress = message[19:]
                return(b"yesMaster")
            else:
                return(b"youWillNeverBeMyMaster")

        elif (message == "otherMessage"):
            return (b"another response from slave node")

        elif (message[:10] == "subvector:"):

            return self.parseSubVectorCommand(message[10:])

        else:
            return(b"ERROR: Could not parse your command to slave node... please try again. \nCommand:" + message)

    def __init__(self, port=5557):

        self.subvectors = list()

        try:
            print("Starting Slave on port:" + str(port))
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:"+str(port))
        except:
            self = Slave(port+1)


        while True:
            # Wait for next request from client
            message = socket.recv()

            socket.send(self.parse(message))

            #  Send reply back to client
            # socket.send(b"I am a slave node.")


slave = Slave()
    