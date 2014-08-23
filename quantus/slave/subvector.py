__author__ = 'andrewtrask'

import numpy as np
import json


class SubVectorSlave():

    def __init__(self, length):
        self.length = length
        self.data = np.zeros(length)

    def setData(self, data):
        self.data = data

    def add(self,value):
        self.data += float(value)
        return 0

    def mul(self,value):
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
        self.mul(value)
        return 0

    def uniform(self,value):
        self.data = np.random.rand(self.length)
        self.mul(value)
        return 0

    def sum(self):
        return str(sum(self.data))

    def getData(self):
        return json.dumps(self.data.tolist())