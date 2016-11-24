#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# run on Python3

'''This time, server can also act like a client, which can say anything, instead of just simply responding.
'''

import socket
from threading import Thread
import sys

PORT = 8081
MAX_CLIENT_SOCKET = 5

def newConnection(sock, addr):
	ip, port = addr
	print('New connection: {0}:{1}'.format(ip, port))

	# process server input in another thread
	selfInputThread = Thread(target=selfInput, args=(sock,))
	selfInputThread.start()

	while True:
		dataFromClient = sock.recv(1024)	# 1K
		word = dataFromClient.decode('utf-8')	# AKA. transformed into unicode

		if (not dataFromClient) or word.strip() == '.exit':	# client send '.exit' as a 'system-level command' to exit the session
			break
		print('[Client {0}:{1}]: {2}'.format(ip, port, word))	# show what the client said		
		#sock.send(b'200 OK\n')

	sock.close()	# never forget to close the socket(in the sub thread)
	print('Close connection: {0}:{1}'.format(ip, port))


def selfInput(sock):
	while True:
		wordFromServer = raw_input('Send words:')
		sock.send(wordFromServer + '\n')


if __name__ == '__main__':
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# tcp socket
	serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	# set the port reusable(unchecked)
	serverSocket.bind( ('127.0.0.1', PORT) )	# bind a certain IP and port
	serverSocket.listen(MAX_CLIENT_SOCKET)	# tcp socket must call listen() method
	print('Listening on port {}...'.format(PORT))

	while True:
		sock, addr = serverSocket.accept()	# block(waiting)
		newConnectionThread = Thread(target=newConnection, args=(sock, addr))
		newConnectionThread.start()	# process in a new thread
		
