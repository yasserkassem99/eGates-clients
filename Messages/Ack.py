from Messages.Message import Message


class Ack(Message):
    def __init__(self):
        super().__init__()
        self.message_type = "ACK_MESSAGE"
        self.message_id = "Random_ID"

    def get_id(self):
        return self.message_id

    def set_id(self, id):
        self.message_id = id
