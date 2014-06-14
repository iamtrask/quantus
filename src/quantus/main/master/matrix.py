__author__ = 'andrewtrask'

from src.quantus.main.master.vector import Vector

class Matrix():


    def __init__(self,slaveSockets,numRows,numCols, data=None):

        self.slaveSockets = slaveSockets
        self.slaveCount = len(slaveSockets)
        self.numRows = numRows
        self.numCols = numCols

        self.rows = list()

        for i in xrange(numRows):
            self.rows.append(Vector(slaveSockets,numCols))

