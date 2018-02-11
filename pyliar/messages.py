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


def create_message(str_in):
    child_classes = Message.__subclasses__()
    for child in child_classes:
        matches = child.regex.findall(str_in)
        if matches:
            # FIXME !! Should instanciate child with array of matched stuffs
            logging.debug("matched: {}".format(child))
            logging.debug("matches: {}".format(matches[0]))
            return child(matches[0])
    return None



class Message:
    regex = None

    def __init__(self):
        self.type = 'UNKN'
        self.id = None

    def to_message_string(self):
        message = pickle.dumps(self)
        return message

    def to_string(self):
        return "Type: {type}, regex: {r}".format(type=self.type, r=self.regex)

    def is_type(self, type):
        return self.type == type


class GuessMessage(Message):
    regex = re.compile(r"^(\d+)[\.,:;x](\d+).*")

    def __init__(self, array):
        super().__init__()
        self.type = 'GUESS'
        self.amount = array[0]
        self.value = array[1]

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {a}, {v}".format(common_part=common_part,
                                                 a=self.amount,
                                                 v=self.value)


class HandMessage(Message):
    regex = re.compile(r"^hand.*")

    def __init__(self, array):
        super().__init__()
        self.type = 'HAND'
        self.hand = array[0]

    def to_string(self):
        common_part = super().to_string()
        return "{common_part} - {hand}".format(common_part=common_part, hand=self.hand)


class StartMessage(Message):
    regex = re.compile(r"^(?:start|play)\s+(?:game|pyliar|liar).*")

    def __init__(self, array):
        super().__init__()
        self.type = 'START'
