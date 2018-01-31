import socket
import logging
import threading
import select

from messages import *

class Game:

    def __init__(self):
        self.game_started = False
        self.player_amount = 0

    def start_game(self):
        self.game_started = True
        logging.info("----------------------------")
        logging.info("Let's play The Liar's Dice !")
        logging.info("----------------------------")
        # TODO get access to players
        # Send them a new hand

class Server:

    def handle_client(self, client_socket):
        self.game.player_amount += 1
        logging.debug("I am in the child thread... - amount {}".format(self.game.player_amount))
        while True:
            data = client_socket.recv(2048)
            logging.info("Received a chunk '{data}'".format(data=data))
            message = decode_message(data)
            if message is not None:
                self.handle_client_message(message)
            else:
                logging.info("Received the following data {}".format(message))

    def handle_client_message(self, msg):
        logging.info("Received the following message: {}".format(msg.to_string()))
        logging.info("{}".format(msg.type))
        if msg.isType('START'):
            logging.info("Start message received from ...")
            self.game.start_game()
        # elif: # TODO other type of message
        else:
            logging.info("This is an unhandled message.. For now !")
            logging.info("What about handling it Jonathan ?!")

    def __init__(self, port):
        self.port = port
        self.game = Game()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', self.port)
        self.sock.bind(server_address)
        logging.info("Starting PyLiar server on {ip_serv}:{port_serv}".format(ip_serv=server_address[0],
                                                                              port_serv=server_address[1]))
        self.sock.listen(1)
        exit_gracefully = False
        self.client_sockets = [self.sock]
        while not exit_gracefully:
            readable, writable, errored = select.select(self.client_sockets, [], [])
            self.handle_sockets(readable)
        self.sock.close()

    def handle_sockets(self, sockets):
        for s in sockets:
            if s is self.sock:
                if not self.game.game_started:
                    self.handle_new_connections()
                else:
                    logging.debug("Handle game started and new connection detected.")

    def handle_new_connections(self):
        client_sock, client_address = self.sock.accept()
        logging.debug("Accepted connection from {}".format(client_address[0]))
        client_handler = threading.Thread(
            target=self.handle_client,
            args=(client_sock,))
        client_handler.start()
        self.client_sockets.append(client_sock)

