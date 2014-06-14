__author__ = 'andrewtrask'

import numpy as np

from quantus.master.subvector_interface import SubVectorMaster

class Vector():

    def __init__(self,slaveSockets,length, data=None):

        self.slaveSockets = slaveSockets
        self.slaveCount = len(slaveSockets)
        self.length = length

        self.subVectors = list()

        for slaveI in range(self.slaveCount):
            subVectorLength = (length/self.slaveCount)
            startIndex = slaveI * subVectorLength

            if(slaveI < self.slaveCount-1):
                endIndex = min(((slaveI + 1) * subVectorLength) - 1,length-1)
            else:
                endIndex = length-1

            self.subVectors.append(SubVectorMaster(self.slaveSockets[slaveI],startIndex,endIndex))


        print ("Vector Created of Length:" + str(length))

    def getData(self):

        data = np.zeros(0)
        print len(data)
        for sv in self.subVectors:
            data = np.concatenate((data, sv.getData()),axis=0)

        return data


    def add(self, value):
        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            response = ""
            for sv in self.subVectors:
                response += str(sv.add(value))

            return response

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.length == self.length):
                print ("executing vector addition")
                for i, sv in enumerate(self.subVectors):
                    sv.add(value.subVectors[i])
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)

        else:
            print(type(value))
            return "ERROR: What kind of object is this?"


    def mul(self, value):
        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):

            response = ""

            for sv in self.subVectors:
                response += str(sv.mul(value))

            return response

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.length == self.length):
                print ("executing vector multiplication")
                for i, sv in enumerate(self.subVectors):
                    sv.mul(value.subVectors[i])
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)


        else:
            print(type(value))
            return "ERROR: What kind of object is this?"

    def pow(self, value):
        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            response = ""
            for sv in self.subVectors:
                response += str(sv.pow(value))
            return response
        else:
            print(type(value))
            return "ERROR: Only scalar power supported"

    def randn(self,value):
        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            response = ""
            for sv in self.subVectors:
                response += str(sv.randn(value))
            return response
        else:
            print(type(value))
            return "ERROR: Only scalar random limit supported"


    def uniform(self, value):
        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            response = ""
            for sv in self.subVectors:
                response += str(sv.uniform(value))
            return response
        else:
            print(type(value))
            return "ERROR: Only scalar random limit supported"


    def sum(self):

        total = 0

        for sv in self.subVectors:
            total += float(sv.sum())

        return total
