#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# run on Python3

'''Simple version:
	Server feed back what client said.
'''

import socket
import time
from threading import Thread

PORT = 8081
MAX_CLIENT_SOCKET = 5

# as the target of a sub thread
def newConnection(sock, addr):
	ip, port = addr
	print('New connection: {0}:{1}'.format(ip, port))
	while True:
		dataFromClient = sock.recv(1024)	# 1K
		word = dataFromClient.decode('utf-8')
		if (not dataFromClient) or word.strip() == 'exit':	# client send 'exit' to exit the session
			break
		else:
			# passively response to client, like HTTP
			sock.send('OK, I receive your message: {0}'.format(word).encode('utf-8'))
	sock.close()	# never forget to close the socket(in the sub thread)
	print('Close connection: {0}:{1}'.format(ip, port))


if __name__ == '__main__':
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# tcp socket
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the port reusable(unchecked)
	serverSocket.bind( ('127.0.0.1', PORT) )	# bind a certain IP and port
	serverSocket.listen(MAX_CLIENT_SOCKET)	# tcp socket must call listen() method
	print('Listening on port {}...'.format(PORT))

	# Forever listen for client socket, so a dead loop
	while True:
		sock, addr = serverSocket.accept()	# block(waiting)
		Thread(target=newConnection, args=(sock, addr)).start()	# process in a new thread
		
