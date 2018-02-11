#!/usr/bin/python3

import getopt
import logging
import sys
import socket
import pickle


from server import Server
from player import Player


class PyLiar:

    DEFAULT_PORT = 1337

    def __init__(self):
        self.server = True
        logging.basicConfig(level='DEBUG',
                            format='[%(levelname)s]  %(asctime)s %(module)s -'
                                   ' %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        self.remote_addr = "127.0.0.1"
        self.port = self.DEFAULT_PORT
        self.sock = None
        self.nickname = None

    def parse_arguments(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hs:c:p:n:", ["server", "client=", "port=", "nickname="])
        except getopt.GetoptError:
            logging.error("Incorrect options given as arguments")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                logging.info("pyliar.py [--server] [[--client=<ip_server>] [--port=<port>] [--nickname=<nick>]]")
                logging.info("Default mode : server")
                sys.exit()
            elif opt in ('-s', '--server'):
                self.server = True
            elif opt in ('-c', '--client'):
                self.remote_addr = arg
                self.server = False
            elif opt in ('-n', '--nickname'):
                self.nickname = arg
            elif opt in ('-p', '--port'):
                self.port = int(arg)

if __name__ == '__main__':
    pyliar_inst = PyLiar()
    pyliar_inst.parse_arguments(sys.argv[1:])
    if pyliar_inst.server:
        liar_serv = Server(pyliar_inst.port)
    else:
        liar_client = Player(pyliar_inst.remote_addr, pyliar_inst.port, pyliar_inst.nickname)
