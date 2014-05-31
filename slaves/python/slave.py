print("Starting Slave")

import time
import zmq

def parse(message):
	print("Received request: %s" % message)

	if (message[:9] == "message"):
		socket.send(b"response from slave node")
	elif (message == "otherMessage"):
		socket.send(b"another response from slave node")
	else:
		socket.send(b"ERROR: Could not parse your command to slave node... please try again.")

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    parse(message)

    #  Send reply back to client
    # socket.send(b"I am a slave node.")