#!/usr/bin/python3

import getopt
import logging
import sys
import socket
import pickle

from messages import *
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

    def parse_arguments(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hs:c:p:", ["server", "client=", "port="])
        except getopt.GetoptError:
            logging.error("Incorrect options given as arguments")
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                logging.info("pyliar.py [--server] [[--client=<ip_server>] [--port=<port>]]")
                logging.info("Default mode : server")
                sys.exit()
            elif opt in ('-s', '--server'):
                self.server = True
            elif opt in ('-c', '--client'):
                self.remote_addr = arg
                self.server = False
            elif opt in ('-p', '--port'):
                self.port = int(arg)

if __name__ == '__main__':
    pyliar_inst = PyLiar()
    pyliar_inst.parse_arguments(sys.argv[1:])
    player = Player()
    message = GuessMessage(2, 5)
    print(message.to_message_string())
    test = pickle.loads(message.to_message_string())
    print(test.type)
    if pyliar_inst.server:
        pyliar_inst.create_server()
    else:
        pyliar_inst.connect_server()
