import time
import zmq



context = zmq.Context()
LISTEN_PORT = 5555
controllerSocket = context.socket(zmq.REP)
controllerSocket.bind("tcp://*:"+str(LISTEN_PORT))

slaveSockets = list()

def addSlave(slavePort):

	tempSocket = context.socket(zmq.REQ)
	tempSocket.RCVTIMEO = 2000
	tempSocket.connect("tcp://localhost:"+str(slavePort))
	tempSocket.send(b"letMeBeYourMaster:"+str(LISTEN_PORT))

	try:
		response = tempSocket.recv()
		print("Slave:" + str(response))
		if(response == "yesMaster"):
			slaveSockets.append(tempSocket)
			return b"Added Slave on Port:" + str(slavePort)
		else:
			return b"Failed to add Slave on Port:" + str(slavePort)
			tempSocket.close()

	except:
		tempSocket.close()
		print("No slave listening on port:" + str(slavePort))
		return "No slave on port:" + str(slavePort)

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
