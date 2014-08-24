__author__ = 'andrewtrask'

import zmq

from quantus.slave.subvector import SubVectorSlave


class Slave:
    masterAddress = "none"

    def createSubVector(self, message):
        index = len(self.subvectors)
        self.subvectors.append(SubVectorSlave(int(message)))
        return (b"" + str(index))

    def iadd(self, index, value):
        return (b"" + str(self.subvectors[index].iadd(value)))

    def iaddVec(self, index, index2):
        self.subvectors[int(index)].data += self.subvectors[int(index2)].data
        return (b"vectors added")

    def imul(self, index, value):
        return (b"" + str(self.subvectors[index].imul(value)))

    def imulVec(self, index, index2):
        self.subvectors[int(index)].data *= self.subvectors[int(index2)].data
        return (b"vectors multiplied elementwise")

    def div(self, index, value):
        return (b"" + str(self.subvectors[index].div(value)))

    def divVec(self, index, index2):
        self.subvectors[int(index)].data /= self.subvectors[int(index2)].data
        return (b"vectors divided elementwise")

    def pow(self, index, value):
        return (b"" + str(self.subvectors[index].pow(value)))

    def randn(self, index, value):
        return (b"" + str(self.subvectors[index].randn(value)))

    def uniform(self, index, value):
        return (b"" + str(self.subvectors[index].uniform(value)))

    def getData(self, index):
        return self.subvectors[int(index)].getData()

    def sum(self, index):
        return self.subvectors[int(index)].sum()

    def dot(self, index, index2):
        prod = self.subvectors[int(index)].dot(self.subvectors[int(index2)])
        # print "Slave:" + str(prod)
        return prod

    def parseSubVectorCommand(self, message):
        """
        Map message of form "command:param1:param2:...:paramN" to internal method

        Parses all parameters into ints.

        :param message: str of form "command:param1:param2:...:paramN"
        """
        components = message.split(":")
        command = components[0]
        params = map(lambda p: int(p), components[1:])

        if command in self.command_dict:
            method = self.command_dict[command]
            return str(method(*params))
        else:
            raise Exception(
                "Invalid SubVector command argument passed to Slave:\n\tCommand:{0}\n\tFullMessage:{1}"
                .format(command, message))

    def parse(self, message):
        # print("Received request: %s" % message)

        if (message[:18] == "letMeBeYourMaster:"):
            if (self.masterAddress == "none"):
                self.masterAddress = message[19:]
                return(b"yesMaster")
            else:
                return (b"youWillNeverBeMyMaster")

        elif (message == "otherMessage"):
            return (b"another response from slave node")

        elif (message[:10] == "subvector:"):
            return self.parseSubVectorCommand(message[10:])

        else:
            return (b"ERROR: Could not parse your command to slave node... please try again. \nCommand:" + message)

    def __init__(self):

        # Map used in parseSubVectorCommand
        self.command_dict = dict(
            create=self.createSubVector,
            iadd=self.iadd,
            iaddVec=self.iaddVec,
            imul=self.imul,
            imulVec=self.imulVec,
            dot=self.dot,
            div=self.div,
            divVec=self.divVec,
            pow=self.pow,
            randn=self.randn,
            uniform=self.uniform,
            getdata=self.getData,
            sum=self.sum
        )

        self.subvectors = list()

    def listen(self, port=5557):
        try:
            print("Starting Slave on port:" + str(port))
            context = zmq.Context()
            socket = context.socket(zmq.REP)
            socket.bind("tcp://*:" + str(port))
        except:
            self.listen(port + 1)

        while True:
            message = socket.recv()

            socket.send(self.parse(message))

            # Send reply back to client
            # socket.send(b"I am a slave node.")
