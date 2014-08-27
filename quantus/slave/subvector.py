__author__ = 'andrewtrask'

import numpy as np
import json


class SubVectorSlave():

    def __init__(self, length):
        self.length = length
        self.data = np.zeros(length)

    def setData(self, data):
        self.data = data
        self.length = len(data)

    def iadd(self,value):
        self.data += float(value)
        return 0

    def imul(self,value):
        self.data *= float(value)
        return 0

    def div(self, value):
        self.data /= float(value)
        return 0

    def pow(self,value):
        self.data = np.power(self.data,float(value))
        return 0

    def randn(self,value):
        self.data = np.random.randn(self.length)
        self.imul(value)
        return 0

    def uniform(self,value):
        self.data = np.random.rand(self.length)
        self.imul(value)
        return 0

    def sum(self):
        return str(sum(self.data))

    def dot(self,subVector):
        output = np.dot(self.data,subVector.data)
        # print "Subvector:" + str(output)
        return output

    def getData(self):
        return json.dumps(self.data.tolist())