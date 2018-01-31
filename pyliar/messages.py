import pickle
import logging
import re


def decode_message(data):
    try:
        message = pickle.loads(data)
        return message
    except pickle.PickleError:
        logging.error("Could not deserialize the data : {data}".format(data=data))
        return None


class Message:
    regex = None

    def __init__(self):
        self.type = 'UNKN'

    def to_message_string(self):
        message = pickle.dumps(self)
        return message

    def to_string(self):
        return "Type: {type}, regex: {r}".format(type=self.type, r=self.regex)

    def is_type(self, type):
        return self.type == type

class GuessMessage(Message):
    regex = r"^(\d+)[\.,:;x](\d+).*"

    def __init__(self, amount, value):
        super().__init__()
        self.type = 'GUESS'
        self.amount = amount
        self.value = value

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {a}, {v}".format(common_part=common_part,
                                                 a=self.amount,
                                                 v=self.value)


class HandMessage(Message):
    regex = r"^hand.*"

    def __init__(self, hand):
        super().__init__()
        self.type = 'HAND'
        self.hand = hand

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {hand}".format(common_part=common_part, hand=self.hand)


class StartMessage(Message):
    regex = r"^start\s+(?:game|pyliar).*"

    def __init__(self):
        super().__init__()
        self.type = 'START'
