__author__ = 'andrewtrask'

import zlib, cPickle as pickle
import json
import numpy as np

class SubVectorMaster():

    def __init__(self, socket, startIndex, endIndex):
        self.socket = socket
        self.startIndex = startIndex
        self.endIndex = endIndex
        self.indexInSlave = int(self.cmd("create:" + str(endIndex - startIndex + 1)))
        print "Created SubVectorMaster at index:" + str(self.indexInSlave)


    def cmd(self,message):
        self.socket.send(b"subvector:" + message)
        return self.socket.recv()

    def add(self, value):
        return self.cmd("add:" + str(self.indexInSlave) + ":" + str(value))

    def mul(self, value):
        return self.cmd("mul:" + str(self.indexInSlave) + ":" + str(value))

    def pow(self, value):
        return self.cmd("pow:" + str(self.indexInSlave) + ":" + str(value))

    def randn(self, value):
        return self.cmd("randn:" + str(self.indexInSlave) + ":" + str(value))

    def uniform(self, value):
        return self.cmd("uniform:" + str(self.indexInSlave) + ":" + str(value))

    def getData(self):
        raw = self.cmd("getdata:"+str(self.indexInSlave))
        return np.array(json.loads(raw))

    def sum(self):
        raw = self.cmd("sum:"+str(self.indexInSlave))
        return float(raw)

