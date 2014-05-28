import time
import zmq

context = zmq.Context()

controllerSocket = context.socket(zmq.REP)
controllerSocket.bind("tcp://*:5555")

slaveSockets = list()

def addSlave(port):
	slaveSockets.append(context.socket(zmq.REQ))
	slaveSockets[len(slaveSockets) - 1].connect("tcp://localhost:"+str(port))
	slaveSockets[len(slaveSockets) - 1].send(b"Hello slave!")
	controllerSocket.send(b"Added Slave on Port:" + str(port))

def countSlaves():
	controllerSocket.send(b""+(str(len(slaveSockets))))

def parse(message):
	
	print("Received request: %s" % message)

	if (message[:9] == "addSlave:"):
		addSlave(message[9:])
	elif (message == "countSlaves"):
		countSlaves()
	else:
		controllerSocket.send(b"ERROR: Could not parse your command... please try again.")



while True:
    #  Wait for next request from client
    message = controllerSocket.recv()
    parse(message)


    #  Send reply back to client
