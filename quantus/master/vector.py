__author__ = 'andrewtrask'

import numpy as np

from quantus.master.subvector_interface import SubVectorMaster

class Vector():

    def __init__(self,name,slaveSockets,length, data=None):

        self.name = name
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

    def __iadd__(self,other):
        self.iadd(other)
        return self

    def iadd(self, value):
        if(isinstance(value,int) or isinstance(value,float)):
            response = ""
            for sv in self.subVectors:
                response += str(sv.iadd(value))

            return response

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.length == self.length):
                print ("executing vector addition")
                for i, sv in enumerate(self.subVectors):
                    sv.iadd(value.subVectors[i])
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)

        else:
            print(type(value))
            print ("ERROR: What kind of object is this?")
            return "ERROR: What kind of object is this?"

    def __imul__(self, other):
        self.imul(other)
        return self

    def imul(self, value):
        if(isinstance(value,int) or isinstance(value,float)):

            response = ""

            for sv in self.subVectors:
                response += str(sv.imul(value))

            return response

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.length == self.length):
                print ("executing vector multiplication")
                for i, sv in enumerate(self.subVectors):
                    sv.imul(value.subVectors[i])
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)
        else:
            print(type(value))
            return "ERROR: What kind of object is this?"

    def __idiv__(self, other):
        self.idiv(other)
        return self

    def idiv(self, value):
        if(isinstance(value, int) or isinstance(value, float)):

            response = ""
            for sv in self.subVectors:
                response += str(sv.div(value))

            return response

        elif(str(type(value)) == "<type 'instance'>"):
            response = ""
            if(value.length == self.length):
                print("executing vector division")
                for i, sv in enumerate(self.subVectors):
                    sv.div(value.subVectors[i])

            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)
        else:
            print(type(value))
            return "ERROR: What kind of object is this?"

    def __pow__(self, power, modulo=None):
        self.pow(power)
        return self

    def pow(self, value):
        if(isinstance(value,int) or isinstance(value,float)):
            response = ""
            for sv in self.subVectors:
                response += str(sv.pow(value))
            return response
        else:
            print(type(value))
            return "ERROR: Only scalar power supported"

    def __neg__(self):
        self.imul(-1)
        return self

    def __sub__(self, other):
        self.iadd(-other)
        return self

    def randn(self,value):
        if(isinstance(value,int) or isinstance(value,float)):
            response = ""
            for sv in self.subVectors:
                response += str(sv.randn(value))
            return response
        else:
            print(type(value))
            return "ERROR: Only scalar random limit supported"


    def uniform(self, value):
        if(isinstance(value,int) or isinstance(value,float)):
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

    def dot(self, value):

        if(str(type(value)) == "<type 'instance'>"):

            if(value.length == self.length):
                # print ("executing vector dot product")
                prod = 0
                for i, sv in enumerate(self.subVectors):
                    prod += (sv.dot(value.subVectors[i]))
                return prod
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)

        else:
            print(type(value))
            print ("ERROR: What kind of object is this?")
            return "ERROR: What kind of object is this?"
