import logging
import numpy
import sys
import select
import pickle
from client import Client
from messages import *
DICE_AMOUNT = 5


class Player(Client):

    def __init__(self, remote_addr, port):
        super().__init__(remote_addr, port)
        self.hand = None
        self.listen_messages()
        # self.hand = numpy.random.randint(1, 6, size=DICE_AMOUNT)
        # logging.debug("New player. His hand is {hand}".format(hand=self.hand))

    def send_message(self, msg):
        self.sock.send(pickle.dumps(msg))

    def listen_messages(self):
        exit_gracefully = False
        self.buffers = [self.sock, sys.stdin]
        while not exit_gracefully:
            readable, writable, errored = select.select(self.buffers, [], [])
            for x in readable:
                if x is self.sock:
                    data = self.sock.recv(256)
                    message = decode_message(data)
                    if message is not None:
                        logging.debug("Received message : {message}".format(message=message))

                elif x is sys.stdin:
                    # handle standard input
                    stuff = sys.stdin.readline()
                    logging.debug("You typed: {}...".format(stuff))
                    # TODO decode 'stuff' and send related message

                    logging.debug("")
                    logging.debug("SENDING START GAME ANYWAY !!")
                    message = StartMessage()
                    self.send_message(message)
