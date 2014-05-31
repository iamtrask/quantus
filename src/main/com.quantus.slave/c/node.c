//  Hello World server

#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <stdlib.h>

int main (int argc, char *argv[])
{
	if(argc != 2) {
		printf("USAGE: ./node tcp://*:<port>\n");
		return 1;
	}

	char *ipAndPort = argv[1];
	
	//  Socket to talk to clients
	void *context = zmq_ctx_new ();
	void *responder = zmq_socket (context, ZMQ_REP);
	int rc = zmq_bind (responder, ipAndPort);
	assert (rc == 0);

	while (1) {
 		char buffer [10];
		zmq_recv (responder, buffer, 10, 0);
		printf ("Received Hello\n");
		          //  Do some 'work'
		zmq_send (responder, buffer, 5, 0);
	}

	free(ipAndPort);
	return 0;
}
