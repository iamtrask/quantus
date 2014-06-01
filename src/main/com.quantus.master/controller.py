import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

while (1 > 0):
    variable = raw_input('quantus>')
    socket.send(variable)
    print(socket.recv())


