import pickle


class Message:
    def __init__(self):
        self.type = 'UNKN'

    def to_message_string(self):
        message = pickle.dumps(self)
        return message


class GuessMessage(Message):
    def __init__(self, amount, value):
        self.type = 'GUESS'
        self.amount = amount
        self.value = value


class HandMessage(Message):
    def __init__(self, hand):
        self.type = 'HAND'
        self.hand = hand
