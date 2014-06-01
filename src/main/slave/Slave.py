import time
import zmq


class Slave:
    masterAddress = "none"


    def parse(self, message):
        print("Received request: %s" % message)

        if (message[:18] == "letMeBeYourMaster:"):
            if (self.masterAddress == "none"):
                self.masterAddress = message[19:]
                self.socket.send(b"yesMaster")
            else:
                self.socket.send(b"youWillNeverBeMyMaster")

        elif (message == "otherMessage"):
            self.socket.send(b"another response from slave node")

        else:
            self.socket.send(b"ERROR: Could not parse your command to slave node... please try again.")


    def __init__(self):
        print("Starting Slave")
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5557")

        while True:
            # Wait for next request from client
            message = self.socket.recv()

            self.parse(message)

            # Send reply back to client
            # socket.send(b"I am a slave node.")


slave = Slave()
	