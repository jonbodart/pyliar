import logging
import numpy

DICE_AMOUNT = 5

class Player:

    def __init__(self):
        self.hand = numpy.random.randint(1, 6, size=DICE_AMOUNT)
        logging.debug("New player. His hand is {hand}".format(hand=self.hand))

