import logging
import numpy


class Player:

    def __init__(self):
        self.hand = numpy.random.randint(1, 6, size=5)
        logging.debug("New player. His hand is {hand}".format(hand=self.hand))

