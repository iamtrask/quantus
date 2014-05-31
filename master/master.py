import time
import zmq

context = zmq.Context()

controllerSocket = context.socket(zmq.REP)
controllerSocket.bind("tcp://*:5555")

slaveSockets = list()

def addSlave(port):

	tempSocket = context.socket(zmq.REQ)
	tempSocket.RCVTIMEO = 2000
	tempSocket.connect("tcp://localhost:"+str(port))
	tempSocket.send(b"Hello slave!")

	try:
		print(tempSocket.recv())
		slaveSockets.append(tempSocket)
		return b"Added Slave on Port:" + str(port)

	except:
		tempSocket.close()
		print("No slave listening on port:" + str(port))
		return "No slave on port:" + str(port)

def countSlaves():

	controllerSocket.send(b""+(str(len(slaveSockets))))


def scanForSlaves():

	for i in range(20):
		addSlave(5556+i)

	controllerSocket.send(b"Total Slaves:"+(str(len(slaveSockets))))

def parse(message):
	
	print("Received request: %s" % message)

	if (message[:9] == "addSlave:"):
		controllerSocket.send((addSlave(message[9:])))
	elif (message == "countSlaves"):
		countSlaves()
	elif (message == "scanForSlaves"):
		scanForSlaves()
	else:
		controllerSocket.send(b"ERROR: Could not parse your command... please try again.")



while True:
    #  Wait for next request from client
    message = controllerSocket.recv()
    parse(message)


    #  Send reply back to client
