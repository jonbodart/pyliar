import logging
import socket

from messages import *

class Client:
    def __init__(self, remote_addr, port, hand):
        self.remote_addr = remote_addr
        self.port = port
        logging.debug("Connecting to remote server '{server}:{port}'".format(server=self.remote_addr, port=self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.remote_addr, self.port))
        self.hand = hand
        while True:
            message = pickle.loads(self.sock.recv(256).decode('utf-8'))
            logging.debug("Received a message with type '{type}'".format(type=message.type))