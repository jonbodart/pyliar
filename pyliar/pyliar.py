#!/usr/bin/python3

import getopt
import logging
import sys
import socket


class PyLiar:

    DEFAULT_PORT = 1337

    def __init__(self):
        self.server = True
        logging.basicConfig(level='DEBUG',
                            format='[%(levelname)s]  %(asctime)s %(module)s -'
                                   ' %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        self.remote_addr = "0.0.0.0"
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
                logging.info("TCImporter.py [--server] [--client=<ip_server>]")
                logging.info("Default mode : server")
                sys.exit()
            elif opt in ('-s', '--server'):
                self.server = True
            elif opt in ('-c', '--client'):
                self.remote_addr = arg
                self.server = False
            elif opt in ('-p', '--port'):
                self.port = arg

    def create_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.port)
        self.sock.bind(server_address)
        logging.info("Starting PyLiar server on {ip_serv}:{port_serv}".format(ip_serv=server_address[0],
                                                                              port_serv=server_address[1]))
        self.sock.listen(1)
        exit_gracefully = False
        while not exit_gracefully:
            logging.info("Wainting for connection")
            connection, client_address = self.sock.accept()
            data = connection.recv(256).decode('utf-8')
            logging.info("Received a chunk {data}".format(data=data))
            exit_gracefully = True
            connection.close()
        self.sock.close()


if __name__ == '__main__':
    pyliar_inst = PyLiar()
    pyliar_inst.parse_arguments(sys.argv[1:])
    if pyliar_inst.server:
        pyliar_inst.create_server()