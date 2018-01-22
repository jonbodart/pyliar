import pickle
import logging

def decode_message(data):
    try:
        message = pickle.loads(data)
        return message
    except pickle.PickleError:
        logging.error("Could not deserialize the data : {data}".format(data=data))
    return None


class Message:
    def __init__(self):
        self.type = 'UNKN'

    def to_message_string(self):
        message = pickle.dumps(self)
        return message

    def to_string(self):
        return "Type: {type}".format(type=self.type)


class GuessMessage(Message):
    def __init__(self, amount, value):
        super().__init__()
        self.type = 'GUESS'
        self.amount = amount
        self.value = value

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {amount},{value}".format(common_part=common_part, amount=self.amount, value=self.value)


class HandMessage(Message):
    def __init__(self, hand):
        super().__init__()
        self.type = 'HAND'
        self.hand = hand

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {hand}".format(common_part=common_part, hand=self.hand)
