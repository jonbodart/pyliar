import logging
import socket
import select
import sys

from messages import *

class Client:
    def __init__(self, remote_addr, port):
        self.remote_addr = remote_addr
        self.port = port
        logging.debug("Connecting to remote server '{server}:{port}'".format(server=self.remote_addr, port=self.port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.remote_addr, self.port))

        exit_gracefully = False
        self.buffers = [self.sock, sys.stdin]
        while not exit_gracefully:
            readable, writable, errored = select.select(self.buffers, [], [])
            for x in readable:
                if x is self.sock:
                    data = self.sock.recv(256)
                    print ("Server responded with", data.decode())
                elif x is sys.stdin:
                    # handle standard input
                    stuff = sys.stdin.readline()
                    logging.debug("message typed: {}".format(stuff))
                    self.sock.send(stuff.encode())
