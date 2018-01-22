import logging
import socket


from messages import *

class Client:
    def __init__(self, remote_addr, port):
        self.remote_addr = remote_addr
        self.port = port
        self.handle_connection()

    def handle_connection(self):
        logging.debug("Connecting to remote server '{server}:{port}'".format(server=self.remote_addr, port=self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.remote_addr, self.port))