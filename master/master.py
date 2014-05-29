import time
import zmq

context = zmq.Context()

controllerSocket = context.socket(zmq.REP)
controllerSocket.bind("tcp://*:5555")

slaveSockets = list()

def addSlave(port):
	tempSocket = context.socket(zmq.REQ)
	tempSocket.RCVTIMEO = 2000
	slaveSockets.append(tempSocket)
	slaveSockets[len(slaveSockets) - 1].connect("tcp://localhost:"+str(port))
	slaveSockets[len(slaveSockets) - 1].send(b"Hello slave!")
	try:
		print(slaveSockets[len(slaveSockets) - 1].recv())
		controllerSocket.send(b"Added Slave on Port:" + str(port))
	except:
		print("No slave listening on port:" + str(port))
		controllerSocket.send(b"No slave on port:" + str(port))

	

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
