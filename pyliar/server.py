import socket
import logging

class Server:

    def __init__(self, port):
        self.port = port
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
            logging.info("Received a chunk '{data}'".format(data=data))
            connection.close()
        self.sock.close()