__author__ = 'andrewtrask'

import numpy as np

from quantus.master.vector import Vector


class Matrix():


    def __init__(self,name,slaveSockets,numRows,numCols, data=None):

        self.name = name
        self.slaveSockets = slaveSockets
        self.slaveCount = len(slaveSockets)
        self.numRows = numRows
        self.numCols = numCols

        self.rows = list()

        for i in xrange(numRows):
            self.rows.append(Vector("matrix:" + str(name) + ":" + str(i),slaveSockets,numCols))

    def div(self, value):

        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            print ("executing scalar matrix division")
            for row in self.rows:
                row /= (value)

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.numRows == self.numRows & value.numCols == self.numCols):
                print ("executing elementwise matrix division")
                for i, sv in enumerate(self.rows):
                    sv /= value.rows[i]
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)

        else:
            print(type(value))
            return "ERROR: What kind of object is this?"

    def add(self, value):

        if(str(type(value)) == "<type 'int'>" or str(type(value)) == "<type 'float'>"):
            for row in self.rows:
                row.add(value)

        elif(str(type(value)) == "<type 'instance'>"):

            response = ""
            if(value.numRows == self.numRows & value.numCols == self.numCols):
                print ("executing elementwise matrix addition")
                for i, sv in enumerate(self.rows):
                    sv.add(value.rows[i])
            else:
                return "ERROR: vectors not of same length " + str(self.length) + " vs " + str(value.length)

        else:
            print(type(value))
            return "ERROR: What kind of object is this?"

    def getRow(self,index):
        return self.rows[index]

    def __getitem__(self,index):
        return self.getRow(index)

    def setRow(self,index,row):
        self.rows[index] = row

    def __setitem__(self, key, value):
        self.setRow(key,value)

    def getData(self):

        data = np.zeros(0)

        for row in self.rows:
            data = np.concatenate((data,row.getData()),axis=0)

        data.shape = (self.numRows,self.numCols)
        return data