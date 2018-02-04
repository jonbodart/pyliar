import socket
import logging
import threading
import select
import errno
from queue import Queue

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

    def handle_disconnection(self, client_socket):
        self.game.player_amount -= 1
        logging.info("Client has disconnected ... / Remaining users : %d", self.game.player_amount)
        self.client_sockets.remove(client_socket)
        client_socket.close()

    def handle_client(self, client_socket):
        self.game.player_amount += 1
        while True:
            data = client_socket.recv(2048)
            if not data:
                break
            message = decode_message(data)
            if message is not None:
                self.handle_client_message(message)
            else:
                logging.info("Received the following data {}".format(message))
                logging.info("This is not a recognized message...")
        self.handle_disconnection(client_socket)

    def handle_client_message(self, msg):
        """
        Handle the messages received from clients.

        :param msg: The received message from client.
        :type msg: Message
        :return: void
        """
        if msg.is_type('START'):
            logging.info("Start message received from ...")
            self.game.start_game()
        # elif: # TODO other type of message
        else:
            logging.info("message received: {}".format(msg.to_string()))
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
            # Handling sockets events.
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

